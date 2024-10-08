+++
title = "VAE 理解までの道のり #2"
date = 2024-03-02T00:53:11+09:00
draft = true
math = true
categories = ["機械学習"]
tags = ["VAE"]
toc = true
+++


## 前回までのおさらい

{{< ref "/post/232c9edf1cb46e/index.md" >}}


## 平均場近似の計算例

以下で簡単に平均場近似についての導入と、その結果求まる事後分布の最適解について説明します。

平均場近似とは事後分布 $p(Z|X)$ を

$$
p(Z|X) \simeq q(Z) = \sum_i q(Z_i)
$$

の形式で表される $q(Z)$ で近似する手法で、変分推論でよく用いられます。変分推論では marginal distribution $p(X)$ が直接計算できないため

$$
\ln p(X) \geq L
$$

となる Evidence Lowe Bound（ELBO）を書き下し、$L$ を最大化することで間接的に $\ln p(X)$ の最大化を実現し最適化問題を解くという流れになっています。


### 近似解


$$
$$


## 平均場近似の計算例

平均場近似の具体例を、ガウス分布を用いて見ていきます。