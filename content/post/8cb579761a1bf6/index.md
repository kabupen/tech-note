+++
title = '不偏分散'
date = 2024-06-29
draft = false
math = true
categories = ["統計検定"]
tags = []
toc = false
+++



## 不偏推定量

統計量 $\hat{\theta}(X)$ が

$$
E[\hat{\theta}(X)] = \theta
$$

を満たすとき、$\theta$ が不偏推定量（unbiased estimator）と呼ばれます。不偏推定量の中で（上式を満たす $\hat{\theta}(X)$ の中で）よい推定量が見つからなかったり、そもそも不偏推定量を構成することができない場合には、最尤法を用いることが一般的です。


## 標本平均

母集団からサンプリングした標本空間を考えます[^1]。まず、標本平均を計算してみます。

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

計算してみると、標本平均 $\bar{X}$ は不偏推定量であることがわかります。


### 覚書

母平均と標本平均を改めて思い出しておきます。母平均 $\mu$ は母集団分布の期待値

$$
E[X] = \int x f(x) ~dx = \mu
$$

のことで、標本平均とは

$$
\bar{X} = \frac{1}{n} \sum_{i=1}^n X_i
$$

のことです[^2]。この辺りを混乱しないようにしておきます。




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