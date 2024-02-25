+++
title = 'Neural Network Diffusion'
date = 2024-02-22T11:08:43+09:00
draft = true
math = true
tags = ["Diffusion model"]
categories = ["arxiv"]
toc = true
+++


## Abstract

画像生成などで成功している Diffusion model を用いて、ニューラルネットワークのパラメータを決定する手法を紹介しています。



## Nerual Network Diffusion

### 概要

本論文で議論している Neural Network Diffusion （p-diff）は2段階の構成になっていて、(1) parameter autoencoder、(2) parameter generation から成ります。

まず autoencoder 部分で、事前学習済モデルのパラメータを latent vector にする学習を行います。次にこの latent vector を正例として通常の latent diffusion model の学習を行います。これらの過程を踏むことで、ランダムノイズからパラメータを生成することができる p-diff を構成することができるというものです。事前学習済モデルのパラメータを latent vector に変換するという以外は、通常の diffusion model の枠組みになっています。

{{< figure src="20240222-111535.png" width="500" >}} 



### Parameter autoencoder

学習に使用したパラメーターはスクラッチで学習した last epoch の重みを使用しているとのことです。この重みを1次元に平坦化して autoencoder への入力とすることで、latent representations を作成します。一つのモデルパラメーターを $s_i$ としたときに、使用するパラメータ群は

$$
S = [s_1, ..., S_k, ..., s_K]
$$

です。これら一つ一つが高次元ベクトルですので、1次元化して $V \in R^{K\times D}$ ベクトルを作成します。損失関数として Mean suquared error を利用し

$$
L = \fraC{1}{K} \sum_{i=1}^K || v_k - \hat{v}_k||^2
$$

と、元々のパラメータを再構成できるように学習を進めます。



## Experiments


### Setup

使用したデータセットは

- MNIST
- CIFAR-10/1000
- STL-10
- Flowers
- F-101

です。また使用したモデルは

- ResNet-18/50
- ViT-Tiny/Base
- ConvNeCt-T/B

です。

autoencoder は 4層の 1D CNN のアーキテクチャを採用しており、使用したパラメータ推定用のモデルそれぞれに対して 200 個のトレーニングサンプル（200 回学習した）を用意しました。ResNet に関してはスクラッチで学習し、Vit-Tiny, ConvNeXt に関しては timm ライブラリで配布されている重みを用いて最終の二層分を fine-tuning しています。


### Results


Table.1 にて、"original"（事前学習済モデル本来のデータ）、"ensemble"（平均をとるアンサンブル）、"p-diff"（本論文の結果）がまとまっています。ここから、ほとんどのケースにおいて従来の精度に匹敵する精度を達成できていることが分かりました。

{{< figure src="20240222-113121.png" width="500" >}} 



## Is P-diff Only Memorizing?


p-diff によって事前学習済モデルと遜色ないパラメーター群を生成できたわけなのですが、事前学習済モデルと p-diff で作成するモデルとの差異を比較していきます。特に、

- p-diff は単純にオリジナルモデルのパラメータを覚えているだけではないか？
- fine-tune モデルとの差異は？

に焦点を当てています。

### Similarity of predictions

類似度（similarity）を以下で定義します：

$$
|P_1^{\rm{wrong}} \cap P_1^{\rm{wrong}}| / |P_1^{\rm{wrong}} \cup P_1^{\rm{wrong}}|
$$

$P^{\rm{wrong}}$ はそのモデルが予測に失敗したバリデーションデータのセットです。"IoU" として捉えることができ、IoU が近いほどモデルの予測が似通っているということを示しています。


Figure. 4(a) では、類似度を(1) 事前学習済モデル同士、(2) p-diff モデル同士、(3) 事前学習済モデルと p-diff モデル同士、(4) 事前学習済モデルと p-diff の最大類似度を見ています。事前学習済モデルとは異なる傾向を示していることから、別の新しいパラメータを作成できている傍証となっています。

Figure. 4(b) では、事前学習済モデルとの最大類似度のモデルがどのような精度を達成しているかをみています。p-diff は類似度が低い傾向にありつつ、元モデル精度（グレー部分）を超えていることが分かります。fine-tuned モデルと比較するとその傾向は異なっており、fine-tune とは別の特徴を捉えた新しいパラメータとなっていることが分かります。

Figure. 4(c) では、各モデルの latent represantation を t-SNE でクラスタリングして見ています。

{{< figure src="20240225-204310.png" width="700" >}} 