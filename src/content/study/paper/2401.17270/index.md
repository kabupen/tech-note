---
title: "YOLO-World: Real-Time Open-Vocabulary Object Detection"
pubDate: 2024-02-20T10:39:08+09:00
categories: []
tags: []
description: ""
---
## Abstract

open vocaburary で物体検知ができるというモデルです。


## Related works

### Open-Vocabulary Object Detection

Open vocabulary とは任意のテキストという意味合いですが、open-vocabulary を用いた物体検知（open-vocabulary detection; OVD）は近年の物体検知でトレンドとなっている技術の一つです。[Detic](https://arxiv.org/pdf/2201.02605.pdf)、[Deformable-DETR](https://arxiv.org/pdf/2010.04159.pdf)、[ovdet](https://arxiv.org/pdf/2302.13996.pdf) などは image-text マッチングの手法を用いて OVD を実現しているモデルです。また [Grounding DINO](https://arxiv.org/abs/2303.05499) は [GLIP](https://arxiv.org/pdf/2112.03857.pdf) と呼ばれる事前学習済モデルを応用したモデルで、OVD の中で有名なモデルの一つです。
しかしこれらのモデルは推論時の計算コストが非常に高く、実プロダクトへの組み込みなどは障壁が高いのが実情です。


## Method

### Pre-training Formulation: Region-Text Pairs

従来の YOLO シリーズではカテゴリ名と bounding box の組み合わせを目的変数として用いていました。YOLO-World ではテキスト$t_i$ （カテゴリ名、名詞からなるフレーズ、物体に関する説明文など）と bounding box $B_i$ との組み合わせを region-text pairs として定義しています。

$$
D = \\{B_i, t_i \\}_{i=1}^{N}
$$



### Model Architecture

モデルのアーキテクチャの概要は Figure.3 で示されています。YOLO-World は

- YOLO Detector
- Text Encoder
- RepVL-PAN

という構成で成り立っています。

{{< figure src="20240220-105647.png" width="600" >}} 



#### YOLO Detector


物体検知部分は YOLOv8 をベースにしています。Darknet backbonse を用いた



#### Text Encoder

入力されたテキストを変換する部分では CLIP で事前学習した Transformer text encoder を使用しています。入力が複数単語からなる文章であった場合、シンプルな n-gram algorithm を用いて単語情報に分解し、それらをエンコーダーに入力しています。単語数を $C$ 、embedding dimensions を $D$ としたときに

$$
W = {\rm{TextEncoder}}(T) \in R^{C\times D}
$$

となるような処理を実装しています。


#### Text Contrastive Head



### Re-parameterizable Vision-Language PAN


Text encoder と YOLO detector で処理された情報は Re-parameterizable Vision-Language PAN（RepVL-PAN）へと入力されます。これにより画像情報 $\\{C_3, C_4, C_5\\}$ を処理して feature pyramids として $\\{P_3, P_4, P_5 \\}$ を計算しています。

{{< figure src="20240220-110645.png" width="300" >}} 



#### Text-guided CSPLayer

CSPLayer を拡張しテキスト情報を扱えるようにしたモジュールとして Text-guided CSPLayer（T-CSPLayer）を導入しています。


#### Image-Pooling Attention 

テキスト情報と画像情報をより詳細に扱うために、Image pooling attenntion と呼ばれる層を導入しています。



### Pre-training Schemes

#### Learning from Region-Text Contrastive Loss.

YOLO-World では mosaic sample $I$ と テキスト $T$ とを受け取って、 $K$ 個のオブジェクトに関する予測値を算出してます。ここでは contrastive loss $L_{con}$ を使用しています。
contrastive loss とは metric learning の一つで、正例は近く負例は遠くになるような学習を進めるための損失関数です。ここでは object-text similarity と object-text assignments を評価指標にしています。また $IoU$ に関する損失値も入れており全体の損失関数としては

$$
L = L_{con} + \lambda (L_{iou} + L_{dfl})
$$

となっています。



## Results


いくつかの結果をまとめてみたいと思います。

まず推論速度についての情報が Figure.1 にまとまっています。NVIDIA　V100 を用いた動作試験では、GLIPや Grounding DINO と同程度の精度（縦軸の値）を維持しながら 50 FPS 超えをマークしています。


{{< figure src="20240220-112706.png" width="300" >}} 


また、COCO データセットにおけるその他 YOLO シリーズとの性能比較ですが、性能劣化することなく OVD を達成できていることが分かります。

{{< figure src="20240220-113027.png" width="300" >}} 


YOLO-World では以上のように、従来の YOLO アーキテクチャをベースとしながら RepVL-APN におけるテキストと画像との融合処理をうまく導入することでリアルタイム性を持った OVD を実現できています。t 

