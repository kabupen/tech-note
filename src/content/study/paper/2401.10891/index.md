+++
title = 'Depth Anything: Unleashing the Power of Large-Scale Unlabeled Data'
date = 2024-01-26
draft = false
math = true
tags = ["Stable Diffusion"]
categories = ["arxiv"]
toc = false
image = "20240217-191535.png"
+++



# Abstract

データ収集を自動化することで大規模データの収集に成功した。


{{< figure src="./20240217-191535.png" width="600" >}} 



# Introduction

単眼深度推定（MDE）は大規模データセットの作成が困難であることから発展が遅れていました。MiDaS はデータ収集の方法などを工夫することで精度をあげた先行研究なのですが、データの偏りなどから zero-shot での推論は精度が制限されていました。本論文ではデータセットを拡張することで、MDE の基盤モデルの作成を目指しています。データの収集方法は

- センサーの利用（LiDAR）
- ステレオマッチング
- SfM

などがありますが、高コストであることから大規模データセットの作成は困難でした。本研究ではラベルなし画像を収集していますが、以下のような利点があります：

- simple and cheap to accquire：簡単かつ安価な取得: モノクロ画像は至る所に存在し、特別な装置を必要とせずに簡単に集めることができる
- diverse：より幅広いシーンをカバーすることができ、汎化性能が期待できる
- easy to annotate：pre-trained MDE モデルを用いてラベルなし画像をアノテーションできるため効率的である


## MiDaS について

まず本研究では MiDaS モデルの再現を行っています（MiDaSのコードがオープンになっていないため）。学習方法はそちらを参考にしていました。MiDaS の問題点はそもそも深度データセットが少なかったため複数のデータセットを用いる必要があったことから、深度のスケールの違いなどに対応する必要があったことです。データセットはMiDaS 論文 Table.1 で示されているように

![image](https://github.com/kabupen/papers/assets/19812756/26a7c913-1fe5-4a88-8c54-df0946c0b353)

様々な形式の ground truth であることに対処しなければならなかったためです。絶対距離、unkown scale、disparity maps（視差マップ）等々に対処するために、効果的な学習ができていなかったのです。



# DepthAnything

## Learning Labeled Images

真値の深度のスケール、シフトに影響されないために affine-invariant loss を使用しています。予測深度と真値との差分を全ピクセルで計算しています：

$$
L = \frac{1}{N_{pix}} \sum_{i}^{N_{pix}} \rho(d_i^\star, d_i)
$$

- $d_i^\star$：予測値
- $d_i$：真値

ここで $\rho$ はaffine-invariant mean で

$$
\begin{aligned}
\hat{d} &= \frac{d_i - t(d)}{s(d)} \\\\
t(d) &= \rm{median}(d) \\\\
s(d) &= \frac{1}{N} \sum |d_i - t(d)|
\end{aligned}
$$

で定義されるように、"正規化" 処理を行った $d$ に対して計算しています。

## Unleashing the Power of Unlabeled Images

この部分が本研究の肝だそうです。

インターネットの発展に伴って大規模データ画像セットの収集だけであれば比較的簡単に行うことができ、ここで問題となるのがどのようにラベルを振っていくかです。ただしそれも既存のモデルがあれば簡単にラベルを振ることも可能です。使用したラベルなしデータが Table.1 にまとまっています：

{{< figure src="./20240217-194220.png" width="300" >}} 

教師モデルを $T$ としたときに（ここでは事前学習した MiDaS）

$$
D^u = \{ (u_i, T(u_i)) \}_{i=1}^N
$$

のように疑似データラベルを自動で作成していきます。このデータで生徒モデル $S$ を学習していきます。
先行研究[^ST++] では、教師モデルの重みを使用するよりも、生徒モデルはそれ自体で re-initialization したほうがよりよい性能になったそうです。


### パイロット版の失敗

ただし本論文では、以上のような自己学習（少量のラベル付きデータと疑似ラベルデータを混ぜて、$T,S$ の学習サイクルを行う手法）は上手く行かなかったとのことでした。論文にもあるように、

> We conjecture that, with already sufficient labeled images in our case, the extra knowledge acquired from additional unlabeled images is rather limited.

今回のタスクでは十分なラベル付きデータが存在しているため、それらを学習したうえで新規の疑似ラベルデータで学習しようとしたときに知見獲得に制限がかかるようです。$S$ と $T$ で同じモデル構造をしているため、正解・不正解の傾向が同じになってしまい学習が進まなくなります。つまり教師も生徒も似た者同士であるため、十分に学習された事前知識から逸脱した知識を習得するのが困難であったようです。

そこで、student model の学習のために、難しいタスクを導入しています。具体的には、学習中に強い augmentation（CutMix、Gaussian blurring） を入れることでより積極的に学習が進むという報告がされています。

- 73 [S++](https://arxiv.org/abs/2106.05095)
- 55 [FixMatch](https://arxiv.org/ftp/arxiv/papers/2001/2001.07685.pdf)


## Semantic-Assisted Perception

セマンティックセグメンテーションの情報を用いることで深度推定がより精度が向上するという先行研究に倣い、DINOv2 を用いた。

$$
L = 1 - \frac{1}{N} \sum \cos (f_i, f_i\prime)
$$

Depth 推定した特徴量と DINOv2の特徴量のコサイン類似度を測定する。

## パイプライン概要

学習のパイプラインが Figure.2 で示されています。

![image](https://github.com/kabupen/papers/assets/19812756/347051da-c7b4-4fc0-951d-fcb7bac210fa)

- labeled/unlabeld image のパイプラインがそれぞれ実線、点線で表現されている
- sup は supervised かな





[^ST++]:St++: Make self-training work better for semi-supervised semantic segmentation.