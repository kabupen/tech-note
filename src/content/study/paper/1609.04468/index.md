+++
title = 'Sampling Generative Networks'
date = 2024-03-23T23:29:58+09:00
draft = false
math = true
categories = ["arxiv"]
tags = ["VAE"]
toc = true
+++


## Introduction

Generative models はニューラルネットワークで表現することができるもので、データセットと同質のサンプルを生成することができるように学習されたものです。generative models ではデータセットを効果的に（圧縮して）表現することのできる latent space を学習しているため、データセットを生成するために latent space からのサンプリング結果を用いることもできます。また latent space では意味を持った数学的処理（semantic operations）も可能です。


## Sampling Techniques


### Interpolation

Genrative models に関する先行研究において、モデルは単純にデータの性質を記憶しているだけではないということが示されています。[Radford et al., 2015](https://arxiv.org/pdf/1511.06434.pdf) の GAN に関する研究によれば、latent vector に対して演算することで word2vec で見たような "King" - "Man" + "Woman" = "Queen" のような現象を引き出すことができると分かっています。

{{< figure src="./20240323-234235.png" width="500" >}}

またこの latent space において、線形補間を行うことで２枚の画像間を滑らかに変形させることもできます。

{{< figure src="./20240324-100928.png" width=500 >}}

本論文では線形補完の代わりに、slerp と呼ばれる高次元空間における球表面の特性を用いた補完方法を提唱しています。これにより、より滑らかに補完することができるようです。


## Attribute Vectors


一般的な generative model ではは高度に構造化された latent spece を学習することができ、ラベル情報（自然言語的の意味情報）を事前に付与しておくことで、その情報を用いた演算も可能になります。例えば笑顔の画像の latent vector から無表情の画像の latent vector を差し引いた "smile vector" を事前に計算し、この情報を無表情の画像に付与して decode することで表情を編集することができるという性質があります[^1]。本論文ではこのように意味的な属性情報を持っているベクトルを attribute vector と呼んでいます。

{{< figure src="./20240324-102201.png" width=500 >}}


[^1]: word2vec でもそうですがつくづく非常に不思議な面白い性質だなと思います。なぜこのようなことが可能なのでしょうか...。