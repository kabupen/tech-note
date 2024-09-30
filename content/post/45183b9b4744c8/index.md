+++
title = '20240327'
date = 2024-03-27T18:54:09+09:00
draft = true
math = true
categories = []
tags = []
toc = true
+++




## Disentangled representation

近年の拡散モデル以前の生成モデル（generative models）とは主に、Variational Autoencoder（VAE）もしくは Generative Adversarial Network（GAN）を指していました。これらのモデルでは入力データを $x$、潜在変数を $z$ としたときに

$$
p(x) = \int p(x|z)p(z) dz
$$

という確率分布からサンプリングを生成しています。通常の VAE や GAN では $x$ の意味を複数の $z$ で表現しています。例えば 
[White, 2016](https://arxiv.org/pdf/1609.04468.pdf) では

{{< figure src="./20240324-234145.png" width=500 >}}

にあるように、"smile" の意味だけを抽出したベクトルを潜在変数 $z$ に加算することで画像を加工できることを示しています。

一方で $\beta-$VAE や InfoGan は単一の $z$ でデータを表現する学習（disentangle な表現学習）を実現しています[^1]。Disentangle については様々な定義があるようですがここでは [^2] に従い、潜在変数のある次元が意味を持ち、その意味に沿った変更があったときは該当の次元だけが変わるような表現を disentangle な表現と定義しておきます。下図の例のように、

{{< figure src=./20240325-000116.png width=150 >}}

とある画像に対する潜在変数のひとつの次元が "shape"（形）に対応し、ひとつの次元が "position" （位置）の意味を持っているような表現のことを指します。





### β-VAE


β-VAE は disentangled factors な性質を持つベクトルを学習できる VAE モデルとして知られています。


## 参考情報

- [Difference between AutoEncoder (AE) and Variational AutoEncoder (VAE)](https://towardsdatascience.com/difference-between-autoencoder-ae-and-variational-autoencoder-vae-ed7be1c038f2)
- [Disentangled な表現の教師なし学習手法の検証](https://tech.preferred.jp/ja/blog/disentangled-represetation/)