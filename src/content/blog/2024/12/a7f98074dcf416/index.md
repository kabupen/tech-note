---
title: 'Diffusers train_text_to_image.py'
description: ""
pubDate: 2024-12-24T09:28:23+09:00
heroImage: '@/assets/blog-placeholder-2.jpg'
tags: []
---
# Diffusers train_text_to_image.py <!-- omit in toc -->

`diffusers` の例で用意されている [train_text_to_image.py](https://github.com/huggingface/diffusers/blob/main/examples/text_to_image/train_text_to_image.py) について、使用しているライブラリから学習ループまでの概観を説明します。

---

## TOC <!-- omit in toc -->

- [初期設定](#初期設定)
  - [Accelerate](#accelerate)
  - [MPSについて](#mpsについて)
  - [is\_main\_process／is\_local\_main\_process](#is_main_processis_local_main_process)
  - [Scheduler](#scheduler)
  - [Tokenizer](#tokenizer)
- [モデル読み込み](#モデル読み込み)
  - [EMA（exponential moving average）](#emaexponential-moving-average)
  - [Optimizer](#optimizer)
- [Dataset](#dataset)
  - [読み込み](#読み込み)
  - [カラム名の定義](#カラム名の定義)
  - [前処理](#前処理)
  - [データローダーの定義](#データローダーの定義)
- [学習](#学習)
  - [prepare](#prepare)
  - [トラッカーの初期化](#トラッカーの初期化)
  - [メインループ](#メインループ)
  - [予測](#予測)

---

## 初期設定

### Accelerate

huggingface が提供するライブラリで、CPU／GPU／TPU などの様々な実行環境で同じコードを用いた実行を簡単に実現するものです。

```python
from accelerate import Accelerator

accelerator = Accelerator(
    gradient_accumulation_steps=args.gradient_accumulation_steps,
    mixed_precision=args.mixed_precision,
    log_with=args.report_to,
    project_config=accelerator_project_config,
)
```


### MPSについて

Apple の Metal Performance Shaders（MPS）バックエンドが使用可能かを確認し、利用可能であれば AMP（Automatic Mixed Precision）を無効にしておきます。MPS は PyTorch のバックエンドであるが、計算にいくつか制約があるため通常の GPU と同様の計算処理ができないです。

```python
# Disable AMP for MPS.
if torch.backends.mps.is_available():
    accelerator.native_amp = False
```


### is_main_process／is_local_main_process

`is_main_process` ではグローバルな主プロセスを指定することができ、`is_local_main_process` ではノードごとの主プロセスを指定することができます。

```python
if accelerator.is_local_main_process:
    ...

if accelerator.is_main_process:
    ...
```


### Scheduler

Diffusion モデルの学習・生成で使用されるノイズスケジューラーを読み込んでいる部分。モデル名とサブフォルダを指定することで、事前学習済みモデルと同じスケジューラーを使用することになります。

```python
from diffusers import DDPMScheduler

noise_scheduler = DDPMScheduler.from_pretrained(
    args.pretrained_model_name_or_path,
    subfolder="scheduler")
```

### Tokenizer

Diffusion モデルのテキストを取り扱うためのトークナイザーを読み込んでいる部分です。

```python
from transformers import CLIPTokenizer

tokenizer = CLIPTokenizer.from_pretrained(
    args.pretrained_model_name_or_path,
    subfolder="tokenizer",
    revision=args.revision
)
```


## モデル読み込み

Diffusion モデルは下図の通り[^1] 

{{< figure src=./20241224-100945.png width=500 >}}

- 画像エンコーダー（VAE）
- テキストエンコーダー（CLIP） 
- Denoising Model（U-Net）

から構成されています。ファインチューニングの際には VAE、CLIP の部分まで学習するかどうか考える必要があり、公式サンプルではこの部分は固定しています。

ここでは ZeRO Stage3 を用いた学習を行いたいのですが、モデルのすべてを DeepSpeed の制御下に置く必要があります。ただしそうなると、パラメーター固定する（学習対象外の）モデルの扱いがうまく扱えないようです。そこで、`CLIPTextModel`、`AutoencoderKL` をロードする際に `zero.Init` を一時的に無効化しておきます。


```python
from transformers.utils import ContextManagers
from accelerate.state import AcceleratorState
from diffusers import AutoencoderKL
from transformers import CLIPTextModel

def deepspeed_zero_init_disabled_context_manager():
    """
    returns either a context list that includes one that will disable zero.Init or an empty context list
    """
    deepspeed_plugin = AcceleratorState().deepspeed_plugin if accelerate.state.is_initialized() else None
    if deepspeed_plugin is None:
        return []

    return [deepspeed_plugin.zero3_init_context_manager(enable=False)]

with ContextManagers(deepspeed_zero_init_disabled_context_manager()):
    text_encoder = CLIPTextModel.from_pretrained(
        args.pretrained_model_name_or_path,
        subfolder="text_encoder",
        revision=args.revision,
        variant=args.variant
    )
    vae = AutoencoderKL.from_pretrained(
        args.pretrained_model_name_or_path,
        subfolder="vae",
        revision=args.revision,
        variant=args.variant
    )

unet = UNet2DConditionModel.from_pretrained(
    args.pretrained_model_name_or_path,
    subfolder="unet",
    revision=args.non_ema_revision
)

# Freeze vae and text_encoder and set unet to trainable
vae.requires_grad_(False)
text_encoder.requires_grad_(False)
unet.train()

```


### EMA（exponential moving average）

広く用いられる Model averaging 手法の一種で、学習中にモデルの重みを指数移動平均（EMA: Exponential Moving Average）として保存する手法です。そのままの重み（raw weights）はノイズを含んでおり直前で使用した学習データに影響されすぎている（過学習している）ため、EMA の重みを使用することで良い推論結果になりやすいです[^2]。学習時は通常のパラメーター更新を行いつつ、推論時には EMA モデルを使用することが多いです。

以下の更新式でパラメーターを更新します。現在 $x_t$ を減衰率 $\gamma$ で減衰させつつ、過去 $x_{t-1}$ の重みを参照するという方法で更新していきます。こうすることで $x_t$ の急激な変化を抑えつつ、ここまでの $x_{t-1}$ の重みをベースにしたモデルを作成することができます。

$$
x_t \leftarrow (1 - \gamma) \cdot x_{t-1} + \gamma \cdot x_t
$$

`diffusers` の [textual_inversion.py](https://github.com/huggingface/diffusers/blob/main/examples/research_projects/intel_opts/textual_inversion_dfq/textual_inversion.py#L270) で実装されています。

```python
# Create EMA for the unet.
if args.use_ema:
    ema_unet = UNet2DConditionModel.from_pretrained(
        args.pretrained_model_name_or_path,
        subfolder="unet",
        revision=args.revision,
        variant=args.variant
    )
    ema_unet = EMAModel(
        ema_unet.parameters(),
        model_cls=UNet2DConditionModel,
        model_config=ema_unet.config,
        foreach=args.foreach_ema,
    )
```


### Optimizer

optimizer の初期化を実施します。

```python
# Initialize the optimizer
if args.use_8bit_adam:
    try:
        import bitsandbytes as bnb
    except ImportError:
        raise ImportError(
            "Please install bitsandbytes to use 8-bit Adam. You can do so by running `pip install bitsandbytes`"
        )

    optimizer_cls = bnb.optim.AdamW8bit
else:
    optimizer_cls = torch.optim.AdamW

optimizer = optimizer_cls(
    unet.parameters(),
    lr=args.learning_rate,
    betas=(args.adam_beta1, args.adam_beta2),
    weight_decay=args.adam_weight_decay,
    eps=args.adam_epsilon,
)
```


## Dataset

### 読み込み

huggingface の `datasets` としてデータを読み込む必要があるため、環境によって条件分岐があります。

データセット名を指定した場合（ex. huggingface上で配布されているなど）：

```python
from datasets import load_dataset

# Downloading and loading a dataset from the hub.
dataset = load_dataset(
    args.dataset_name,
    args.dataset_config_name,
    cache_dir=args.cache_dir,
    data_dir=args.train_data_dir,
)
```

ローカルのデータを `datasets` に変換しつつ読み込む場合（パターン①）：

- `datadir/{train, test}/**/image001.jpg` のようなディレクトリ構造を想定
- `datadir` までのパスを指定することで train/test 分割しながら読み込んでくれる

```python
from datasets import load_dataset

data_files = {}
if args.train_data_dir is not None:
    data_files["train"] = os.path.join(args.train_data_dir, "**")

dataset = load_dataset(
    "imagefolder",
    data_files=data_files,
    cache_dir=args.cache_dir,
)
# See more about loading custom images at
# https://huggingface.co/docs/datasets/v2.4.0/en/image_load#imagefolder
```

ローカルのデータを `datasets` に変換しつつ読み込む場合（パターン②）：

- 画像とキャプションを対にした JSON ファイルを想定する場合
- `{"image": "/path/to/image.jpg", "text": "this is a man"}` のような jsonl を指定する

```python
from datasets import load_dataset, Features, Image, Value

data_files = {}
if args.train_data_dir is not None:
    data_files["train"] = os.path.join(args.train_data_dir, "**")

dataset = load_dataset(
    "json",
    data_files="/path/to/file.json"
)

features = Features({
        "image": Image(),
        "text": Value("string")
})
dataset = dataset.cast(features)
```

### カラム名の定義

text-to-image の Diffusion モデルでは画像とキャプションが必要になり、それらのカラム名を取得しておきます。

```python
# Preprocessing the datasets.
# We need to tokenize inputs and targets.
column_names = dataset["train"].column_names

# 6. Get the column names for input/target.
dataset_columns = DATASET_NAME_MAPPING.get(args.dataset_name, None)
if args.image_column is None:
    image_column = dataset_columns[0] if dataset_columns is not None else column_names[0]
else:
    image_column = args.image_column
    if image_column not in column_names:
        raise ValueError(
            f"--image_column' value '{args.image_column}' needs to be one of: {', '.join(column_names)}"
        )
if args.caption_column is None:
    caption_column = dataset_columns[1] if dataset_columns is not None else column_names[1]
else:
    caption_column = args.caption_column
    if caption_column not in column_names:
        raise ValueError(
            f"--caption_column' value '{args.caption_column}' needs to be one of: {', '.join(column_names)}"
        )
```


### 前処理

データの前処理を行い、新しいデータ構造として

- pixel_values に前処理済み画像
- input_ids にトークン化済みキャプション

をそれぞれ持つデータとします。`accelerator.main_process_first()` を用いることで、最初のプロセスでのみ実行することで並列処理における同期を取ります。

```python
from torchvision import transforms

def tokenize_captions(examples, is_train=True):
    captions = []
    for caption in examples[caption_column]:
        if isinstance(caption, str):
            captions.append(caption)
        elif isinstance(caption, (list, np.ndarray)):
            # take a random caption if there are multiple
            captions.append(random.choice(caption) if is_train else caption[0])
        else:
            raise ValueError(
                f"Caption column `{caption_column}` should contain either strings or lists of strings."
            )
    inputs = tokenizer(
        captions, max_length=tokenizer.model_max_length, padding="max_length", truncation=True, return_tensors="pt"
    )
    return inputs.input_ids

# Preprocessing the datasets.
train_transforms = transforms.Compose(
    [
        transforms.Resize(args.resolution, interpolation=transforms.InterpolationMode.BILINEAR),
        transforms.CenterCrop(args.resolution) if args.center_crop else transforms.RandomCrop(args.resolution),
        transforms.RandomHorizontalFlip() if args.random_flip else transforms.Lambda(lambda x: x),
        transforms.ToTensor(),
        transforms.Normalize([0.5], [0.5]),
    ]
)

def preprocess_train(examples):
    images = [image.convert("RGB") for image in examples[image_column]]
    examples["pixel_values"] = [train_transforms(image) for image in images]
    examples["input_ids"] = tokenize_captions(examples)
    return examples

with accelerator.main_process_first():
    if args.max_train_samples is not None:
        dataset["train"] = dataset["train"].shuffle(seed=args.seed).select(range(args.max_train_samples))
    # Set the training transforms
    train_dataset = dataset["train"].with_transform(preprocess_train)
```


### データローダーの定義

```python
def collate_fn(examples):
    pixel_values = torch.stack([example["pixel_values"] for example in examples])
    pixel_values = pixel_values.to(memory_format=torch.contiguous_format).float()
    input_ids = torch.stack([example["input_ids"] for example in examples])
    return {"pixel_values": pixel_values, "input_ids": input_ids}

# DataLoaders creation:
train_dataloader = torch.utils.data.DataLoader(
    train_dataset,
    shuffle=True,
    collate_fn=collate_fn,
    batch_size=args.train_batch_size,
    num_workers=args.dataloader_num_workers,
)
```


## 学習


### prepare

`accelerate` ライブラリを用いた分散学習の宣言を行います。

```python
unet, optimizer, train_dataloader, lr_scheduler = accelerator.prepare(
    unet, optimizer, train_dataloader, lr_scheduler
)
```





### トラッカーの初期化

分散学習環境でのメトリクスなどをトラッキングするための機能（`tensorboard`, `wandb` など）を初期化します。

```python
if accelerator.is_main_process:
    tracker_config = dict(vars(args))
    tracker_config.pop("validation_prompts")
    accelerator.init_trackers(args.tracker_project_name, tracker_config)
```



### メインループ

エポック、ステップのループです。

```python
for epoch in range(first_epoch, args.num_train_epochs):
    train_loss = 0.0
    for step, batch in enumerate(train_dataloader):
```

gradient accumulation も `accelerate` を使用すると分散環境でも同期を管理してくれます。

```python
with accelerator.accumulate(unet):
    ...
```

画像を潜在空間にエンコードしておきます。

```python
latents = vae.encode(batch["pixel_values"].to(weight_dtype)).latent_dist.sample()
latents = latents * vae.config.scaling_factor
```


潜在空間の画像サイズと同じガウシアンノイズを生成します。

```python
noise = torch.randn_like(latents)
if args.noise_offset:
    noise += args.noise_offset * torch.randn((latents.shape[0], latents.shape[1], 1, 1), device=latents.device)
if args.input_perturbation:
    new_noise = noise + args.input_perturbation * torch.randn_like(noise)
```


作成したノイズを元に、diffusion model における forward process を行います。forward process では

$$
x_t = \sqrt{\alpha_t} x_0 + \sqrt{1-\alpha_t} \epsilon
$$

に従って、初期画像 $x_0$ に時刻分（timestep分）ノイズを付加します。$\alpha_t$ は時刻が進むほど 0 に近づく値であり、十分に大きい時刻が経過すると

$$
x_t \simeq \epsilon
$$

となり、完全なノイズになります。実際の学習では $x_T$ から $x_0$ を予測するタスクを解くのではなく、$x_t$ から $x_{t-1}$ を解くタスクを学習させます。またどれだけのノイズを付加するかはバッチごとにランダムに変えることで、どのような時刻にも対応できる汎化性能をもったモデルとしています。 

```python
# Sample a random timestep for each image
timesteps = torch.randint(0, noise_scheduler.config.num_train_timesteps, (bsz,), device=latents.device)
timesteps = timesteps.long()

# Add noise to the latents according to the noise magnitude at each timestep
# (this is the forward diffusion process)
if args.input_perturbation:
    noisy_latents = noise_scheduler.add_noise(latents, new_noise, timesteps)
else:
    noisy_latents = noise_scheduler.add_noise(latents, noise, timesteps)
```



### 予測

前時刻の出力となるように逆拡散過程（U-Net の出力計算）を行い、損失関数を計算します。

```python
# Predict the noise residual and compute loss
model_pred = unet(noisy_latents, timesteps, encoder_hidden_states, return_dict=False)[0]

if args.snr_gamma is None:
    loss = F.mse_loss(model_pred.float(), target.float(), reduction="mean")
else:
    # Compute loss-weights as per Section 3.4 of https://arxiv.org/abs/2303.09556.
    # Since we predict the noise instead of x_0, the original formulation is slightly changed.
    # This is discussed in Section 4.2 of the same paper.
    snr = compute_snr(noise_scheduler, timesteps)
    mse_loss_weights = torch.stack([snr, args.snr_gamma * torch.ones_like(timesteps)], dim=1).min(
        dim=1
    )[0]
    if noise_scheduler.config.prediction_type == "epsilon":
        mse_loss_weights = mse_loss_weights / snr
    elif noise_scheduler.config.prediction_type == "v_prediction":
        mse_loss_weights = mse_loss_weights / (snr + 1)

    loss = F.mse_loss(model_pred.float(), target.float(), reduction="none")
    loss = loss.mean(dim=list(range(1, len(loss.shape)))) * mse_loss_weights
    loss = loss.mean()
```



[^1]: [High-Resolution Image Synthesis with Latent Diffusion Models](https://arxiv.org/pdf/2112.10752)
[^2]: [Rethinking How to Train Diffusion Models](https://developer.nvidia.com/blog/rethinking-how-to-train-diffusion-models/#exponential_moving_averages)