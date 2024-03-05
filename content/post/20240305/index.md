+++
title = '鳥コンペ　(Cornell Birdcall Identification)'
date = 2024-03-05T23:36:12+09:00
draft = true
math = true
categories = ["Kaggle"]
tags = []
toc = true
+++


## コンペ概要



## [1st Place Solution](https://www.kaggle.com/competitions/birdsong-recognition/discussion/183208)


#### Model

- デフォルトの SED (Sound Event Detection) モデル（[公開 notebook](https://www.kaggle.com/code/hidehisaarai1213/introduction-to-sound-event-detection/notebook)）では 80 million パラメータがあるため、モデルを小さくする試みを行った
  - [PANNs](https://arxiv.org/abs/1912.10211) のモデルがベースらしい
  - 少数データでの過学習を抑制する目的

- 4 fold w/o mixup
- 4 fold w/ mixup
- 5 fold w/o mixup

### Data Augmentation

- pink noise
- gaussian noise
- gaussian snr
- gain

#### Training

- Cosine Annealing Scheduler with warmup
- AdamW with weight_decay 0.01
- batch size 28
- Mixup (on 4 of the final models)
- 50 epochs for non-mixup models and 100 epochs for mixup models
- SpecAugmentation enabled
- 30 second audio clips during training and evaluating on 2 30 second clips per audio.

#### Ensemble

- LB ベースでモデルを選定し、13モデルのアンサンブルを実施
  - ただ時間の兼ね合いで個々のモデルについて深追いはできなかった、ensemble したらスコアが伸びるだろうという考えを信じてやっていた

#### コード関連

- https://www.kaggle.com/code/hidehisaarai1213/introduction-to-sound-event-detection
- https://github.com/ryanwongsa/kaggle-birdsong-recognition
  - [mixup.py](https://github.com/ryanwongsa/kaggle-birdsong-recognition/blob/master/src/augmentations/mixup.py)


## [3rd Place Solution](https://www.kaggle.com/competitions/birdsong-recognition/discussion/183199)


### Model

- ResNeXt50, 101

### Data Augmentation

- Gaussian noise
- Background noise
  - 鳥の鳴き声が入っていないデータを持ってきた
- Modified mixup
  - 適用確率は 50% に設定
- cropping
  - 適当にクロッピングするのではなく、何らかの条件に応じた cropping を実施


## [4th Place Solution](https://www.kaggle.com/competitions/birdsong-recognition/discussion/183339)

#### Model

- EfficientNetB3, 4, 5 pretrained on [noisy student](https://github.com/rwightman/gen-efficientnet-pytorch)
  - 元論文：https://arxiv.org/abs/1911.04252
- 分類用の Head をいくつか試したが、結局シンプルなもの（2Layer Dropout --> Linear --> ReLU ）が一番良かった
- [Multi-Sample Dropout](https://arxiv.org/pdf/1905.09788.pdf) が効いたらしい

#### Data

- CNN で feature extraction したが、3チャンネルにする必要があった
  - Logmel を3回重ねた (good baseline)
- not work
  - frequency encoding
    - 過去コンペで使用されていたもの（[code](https://www.kaggle.com/c/freesound-audio-tagging-2019/discussion/97926)）
    - 発想としては、CNN はposition-invariant であるが、スペクトログラムそれ自体は画像のようで画像ではなく y-axis の並び順が重要であるとのこと [^1]
  - loudness
  - spectral centroid

#### Data Augmentation

- 2%程度精度を向上させている

#### Training

- Adam
- ReduceLROnPlateau

#### Ensemble

- 14実験（70モデル）のアンサンブルを実施
  - https://www.kaggle.com/code/vladimirsydor/4-th-place-solution-inference-and-training-tips/notebook#ALL-My-Models



## [6th Place Solution](https://www.kaggle.com/competitions/birdsong-recognition/discussion/183204)


- Trust LB した
  - よい local での validation ができなかったため（train/test に大きな乖離が見られていたらしい）、ignoce CV の戦略を採った


#### 1st stage

##### Model
- PANN モデル
- attention pooling, max poolint 
  - weak prediction を作成するために利用した

##### Data
##### Data Augmentation

- NoiseInjection (max noise amp. 0.0.4)
- PitchShift (max pitch level 3)
- RandomVolume (max db level 4)

##### Training

- Adam
- CosineAnnealing


## 感想

- optimizer, scheduler は特にベースラインから動かしてなさそう（Adam, etc）
- Attention が使用されている([code](https://www.kaggle.com/code/hidehisaarai1213/introduction-to-sound-event-detection))
- mixup が多く使用されていた（[code](https://github.com/ryanwongsa/kaggle-birdsong-recognition/blob/master/src/augmentations/mixup.py)）
- EfficientNet の noisy student が使用されていた
- Dropout が単純に効く
  - Multi-sample dropout ?
- モデルをたくさん試す、ということは効いていない印象




[^1]: CNN の inductive bias について議論しているのかも。CNN自体 global feature（位置関係）は積極的には取りいれていないのでそれを何とかしたいという話か。