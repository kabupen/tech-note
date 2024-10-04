+++
title = '不偏分散'
date = 2024-06-29
draft = false
math = true
tags = ["統計"]
toc = false
+++

# はじめに

統計調査では母集団の性質を調べるためにサンプルを抽出しますが、母数（母平均や母分散）は実際にはわからないため、このときに得られたサンプルに従って各統計量が計算されます。さてこれらの統計量はどのような性質を持っているのか、本記事で議論してみます。


## 不偏推定量

統計量 $\hat{\theta}(X)$ が

$$
E[\hat{\theta}(X)] = \theta
$$

を満たすとき、$\theta$ を不偏推定量（unbiased estimator）と呼びます。不偏推定量の中で（上式を満たす $\hat{\theta}(X)$ の中で）よい推定量が見つからなかったり、そもそも不偏推定量を構成することができない場合には、最尤法を用いることが一般的です。


## 標本平均

平均が $\mu$、分散が $\sigma^2$ の母集団からサンプリングした標本空間を考えます[^1]。まず、標本平均を計算してみます。

$$
\bar{X} = \frac{1}{n} \sum_{i=1}^n X_i
$$

さて、この標本平均が不偏推定量かどうかを考えてみます。

$$
\begin{aligned}
E[\bar{X}] &= E \left[\frac{1}{n} \sum_{i=1}^n X_i \right] \\\\ 
&= \frac{1}{n}\sum_{i=1}^n E \left[  X_i \right]  \\\\
&= \frac{1}{n}\sum_{i=1}^n \mu \\\\
&= \mu
\end{aligned}
$$

計算してみると、標本平均 $\bar{X}$ は不偏推定量であることがわかります[^2]。

ここで「母平均 $\mu$ は分からないのに $\bar{X}$ の期待値を計算すれば算出できた、じゃあ分かってるじゃん」と思ったりするのですが、期待値の計算のためには

$$
E[X] = \mu
$$

を使っているので、そもそも母平均が分からなければ右辺の具体的な数値も分からないままです。ここでの主張は、理論的に標本平均の期待値は母平均に等しいので、母平均の推定量として使用するにはある種の妥当性があるということです。


### 用語の整理


母平均（単に平均とも）$\mu$ は母集団の期待値

$$
E[X] = \int x f(x) ~dx = \mu
$$

のことです。標本平均とは

$$
\bar{X} = \frac{1}{n} \sum_{i=1}^n X_i
$$

のことです。この辺りを混乱しないようにしておきます。



## 不偏分散

次に標本分散について考えてみます。標本分散は $s^2$ で表されることが多く、

$$
s^2 = \frac{1}{n} \sum_{i=1}^n (X_i - \bar{X})^2
$$

で計算されます。さて、この標本分散が不偏推定量かどうかを考えてみます。


$$
\begin{aligned}
E[s^2] 
&= E \left[\frac{1}{n} \sum_{i=1}^n (X_i - \bar{X})^2 \right] \\\\ 
&= \frac{1}{n} \sum_{i=1}^n E \left[(X_i - \bar{X})^2 \right] \\\\ 
&= \frac{1}{n} \sum_{i=1}^n E \left[(X_i - \mu + \mu - \bar{X})^2 \right] \\\\ 
&= \frac{1}{n} \sum_{i=1}^n E \left[(X_i - \mu)^2  + 2 (X_i - \mu)(\mu - \bar{X}) + (\mu - \bar{X})^2 \right] \\\\ 
\end{aligned}
$$

ここからひたすら愚直に計算してみます。

$$
\begin{aligned}
E [(X_i - \mu)^2] 
&= E[ X_i^2 - 2X_i\mu + \mu^2] \\\\ 
&= E[ X_i^2] - 2E[X_i]\mu + \mu^2 \\\\ 
&= \sigma^2 + \mu^2 - 2\mu^2 + \mu^2 \\\\ 
&= \sigma^2
\end{aligned}
$$

ここでは $V[X] = \sigma^2 = E[X^2] - (E[X])^2$ の公式を使って $E[X_i^2]$ を展開しています。
続いて、

$$
\begin{aligned}
E [(X_i - \mu)(\mu - \bar{X})] 
&= E[ X_i\mu - X_i\bar{X} - \mu^2 + \mu\bar{X}] \\\\ 
&= E[ X_i]\mu - E[X_i\bar{X}] - \mu^2 + \mu E[\bar{X}] \\\\ 
&= \mu^2 - \left( E \left[\frac{1}{n}X_i^2 + \frac{1}{n}X_i (n-1)X_j \right]\right) - \mu^2 + \mu^2 \\\\ 
&= \mu^2 - \left( \frac{1}{n} (\sigma^2 + \mu^2) + \frac{1}{n}(n-1)\mu^2 \right) - \mu^2 + \mu^2 \\\\ 
&= - \frac{1}{n}\sigma^2
\end{aligned}
$$

ここでは、$X_i\bar{X}$ の計算に注意しています。
最後に、

$$
\begin{aligned}
E [(\mu - \bar{X})^2] 
&= E[ \mu^2 - 2\mu\bar{X} + \bar{X}^2] \\\\ 
&= \mu^2 - 2\mu^2 + \frac{1}{n^2} \left( nE[X_i^2] + (n^2-n) E[X_i]E[X_j] \right) \\\\ 
&= \mu^2 + \frac{1}{n}\sigma^2
\end{aligned}
$$

です。これらを合わせて計算すると


$$
E \left[s^2 = \frac{1}{n}\sum_{i=1}^n (X_i - \bar{X})^2 \right]  = \frac{n-1}{n} \sigma^2
$$

となります。

ここで不偏推定量の条件を思い出すと

$$
E[s^2] = \sigma^2
$$

にならないとだめなので、ということで標本分散を次のように修正します。


$$
\begin{aligned}
E \left[ \frac{1}{n}\sum_{i=1}^n (X_i - \bar{X})^2 \right] &= \frac{n-1}{n} \sigma^2 \\\\
E \left[ \frac{n}{n-1} \times \frac{1}{n}\sum_{i=1}^n (X_i - \bar{X})^2 \right] &= \sigma^2 \\\\
E \left[ \frac{1}{n-1} \sum_{i=1}^n (X_i - \bar{X})^2 \right] &= \sigma^2 \\\\
\end{aligned}
$$


から、


$$
\begin{aligned}
s^2 = \frac{1}{n-1} \sum_{i=1}^n (X_i - \bar{X})^2
\end{aligned}
$$

が不偏標本分散であることが導出できました。


## 結論


「不偏標本分散は $n-1$ で割る」というフレーズは巷に溢れていますが、あまり深く考えず計算したらそうなる、ということに留めておくのがいいと思います。

そして標本分散を

$$
\begin{aligned}
s^2 = \frac{1}{n} \sum_{i=1}^n (X_i - \bar{X})^2
\end{aligned}
$$

と計算しても **間違いではない** ということは改めて強調しておこうと思います。単にそれが不偏推定量ではないだけです。
解析によっては特に問題はないと思いますし、データの概要を把握するであったりする分には特に問題は生じないです。



[^1]: ひらたく考えると、 実験データを取得してそのデータを使った計算を行うということです。
[^2]: 自分はよく $\bar{X} = \mu$ という短絡的な勘違いをしがちです...。正しくは $E[\bar{X}] = \mu$ です。