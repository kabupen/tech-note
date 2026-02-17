---
title: "mixup: Beyond Empirical Risk Minimization"
pubDate: 2024-03-06T09:58:44+09:00
categories: ["arxiv"]
tags: []
description: ""
---
## Introduction

ニューラルネットワークの学習が成功している要因として、本論文中では empirical risk minimization（経験的損失最小化; ERM）とモデルサイズとデータサイズが比例している関係にあることを挙げています。

教師あり学習ではニューラルネットワークは目的変数 $y$ を予測値 $f(x,\theta)$ との乖離度合いを損失関数で表し、損失関数を最適化する問題としてパラメータ更新を進めていきます。損失関数を $\ell(y, f(x,\theta))$ とすると、損失の期待値を最適化する問題（汎化誤差）

$$
\argmin_\theta E[\ell(y, f(x,\theta))]
$$

で理想的に損失関数（誤差）を最適化できるのですが、実際には観測されたデータのみしか情報として用いれないため、以下で定義される

$$
\argmin_\theta \frac{1}{n} \sum_i \ell(y_i, f(x_i,\theta))
$$

の訓練誤差（経験誤差）の最適化問題を解くのが一般的です。これが経験損失最小化（ERM）と呼ばれる原理で、現在のニューラルネットワークの学習の枠組みでうまくいっています。ただしネットワークが訓練データを記憶することを許しているため、汎化性能があるかどうかを担保する学習にはなっていないという問題があり、本論文中ではこれらの問題に対処する手法として、mixup を導入しています。


### MixUp

説明変数の組 $(x_i, x_j)$ と目的変数の組 $(y_i, y_j)$ を用意し、以下の関係式で新しいデータを用意する手法を mixup として提案しています。

$$
\begin{aligned}
\bar{x} &= \lambda x_i + (1-\lambda) x_j \\\\
\bar{y} &= \lambda y_i + (1-\lambda) y_j
\end{aligned}
$$




## 実装について

Mixup の実装について、例えば PANNs の [ソース](https://github.com/qiuqiangkong/audioset_tagging_cnn/blob/d2f4b8c18eab44737fcc0de1248ae21eb43f6aa4/utils/utilities.py#L117) に簡単な実装があります。





## 参考文献

- [深層学習および機械学習の数理](https://ibis.t.u-tokyo.ac.jp/suzuki/lecture/2020/intensive2/%E8%AC%9B%E7%BE%A91.pdf)