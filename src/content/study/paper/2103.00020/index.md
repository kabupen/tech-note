---
title: "Learning Transferable Visual Models From Natural Language Supervision"
pubDate: 2024-02-21T09:17:53+09:00
categories: ["arxiv"]
tags: []
description: ""
---
## Abstract


Contrastive Language-Image Pre-training（CLIP）は基盤モデルとして、現在様々なモデルで使用されている手法となっています。非常にシンプルな手法ながら zero-shot で非常に良い精度を達成できているところが素晴らしいモデルです。大規模データセットの構築と、対照学習が CLIP の肝と言えます。


## Approach


CLIP は学習手法として提案されていますが、一般的には「CLIP モデル」として認識されていることが多いと思います。ここでもモデル名として議論していこうと思います。CLIP のモデルアーキテクチャ概要は次のとおりです。

{{< figure src="20240221-093440.png" width="600" >}} 

一般的な画像分類モデルでは画像特徴量を使用して分類タスクを学習していきますが、CLIP では対照学習（contrastive learning）と呼ばれる手法を用いて、画像とテキストの正しいペアを学習していきます。

$N$ 組の画像・テキストペアが与えられたときに、CLIP は $N \times N$ の組み合わせについて学習を行っていきます。このときに、正しい組み合わせは $N$ 個（上図における対角線の青色部分）、誤っている組み合わせは $N^2 -N$ 個（それ以外の白い部分）となります。Image encoder と Text encoder で作成した特徴量ベクトルの類似度を使って損失関数を計算していきます。


### Creating a Sufficiently Large Dataset


MS-COCO、Visual Genome、YFCC100M といった既存のデータセットでは不十分であったため、本論文では新しいデータセットの構築を行っています。400 million（4億枚）の画像とテキストが対になったWebImageText（WIT）データセットを構築しています。

このデータセットは公開されていませんが、インターネットからクロールして取得されたデータセットであるようです。


###  Choosing and Scaling a Model

Image encoder として、ResNet と Vision Transformer（ViT）、Text encoder として Transformer を使用しています。本論文では大規模データセットを用意しているため過学習の問題が生じないと考えられたことから、Image encoder は scratch で学習しています（ImageNet 等の重みで初期化されていません）。


### Loss function

学習の擬似コードが Figure.3 で示されています。
画像の埋め込みから損失関数の計算までの説明がなされています。

{{< figure src="20240221-094834.png" width="300" >}} 


画像、テキストをそれぞれの encoder で変換したベクトルを $I_i, T_j$ とすると、CLIP では類似度スコアとして以下の形式のものが使用されます。

$$
s_{ij} = \cos (I_i, T_j) \times \exp (t)
$$

$t$ は学習可能な温度パラメーター（temperature parameter）で、softmax で出力された際に分布をどの程度急峻にするかを調整するためのパラメータです。
損失関数は cross entropy を使用していますが、画像 $i$ とテキスト $j$ に関して2種類の計算を行います。例として画像 $i$ に関しての損失関数の計算方法ですが、以下の図の赤枠で囲った方向（行方向）に対して softmax を適用し $p_{i}$ を計算します。

{{< figure src="20240221-104039.png" width="400" >}} 

$N$ 行方向で計算したものが

$$
L_I = - \sum_{i=1}^N y_i \log p_i
$$


画像方向での損失関数で、同様に列方向での損失関数も計算しておきます。実際に学習に使用する損失関数は

$$
L = (L_I + L_T)/2
$$

と平均をとった損失関数を使用します。