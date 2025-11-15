+++
title = '超幾何分布について'
date = 2024-10-05
draft = false
categories = []
tags = ["統計"]
+++


# 超幾何分布


非復元抽出に関する確率分布で、$M$ 個の赤いボールと $N-M$ 個の白いボールが入っている箱の中から $K$ 個のボールを非復元抽出したときに、$X$ 個が赤いボールであったときに $X$ が従う確率分布が超幾何分布になります。


$$
\binom{M}{X}\binom{N-M}{K-X} / \binom{N}{K}
$$


## 和が1になる


$$
\sum_{x=0}^K P(X=x|M,N,K) = 1 
$$

を証明します[^1]。そのために、


$$
(a+b)^n = (a+b)^{m}(a+b)^{n-m}
$$


の二項展開を用います。左辺は

$$
\sum_{k=0}^n \binom{n}{k} a^k b^{n-k}
$$

です。右辺を同様に計算して $a^{k}b^{n-k}$ の係数比較を行うのが大まかな流れです。右辺は

$$
\sum_{x=0}^m \binom{m}{x} a^xb^{m-x} \sum_{y=0}^{n-m} \binom{n-m}{y} a^yb^{n-m-y} \\\\
= \sum_{x=0}^m \sum_{y=0}^{n-m} \binom{m}{x} \binom{n-m}{y}a^{x+y}b^{n-x-y}
$$


となります。$x+y=k$ と置き換えれば右辺にも $a^{k}b^{n-k}$ が現れるのですが、このときに係数の計算に少し注意しながら次のように変形していきます。

$$
\sum_{x=0}^m \sum_{y=0}^{n-m} \binom{m}{x} \binom{n-m}{y}a^{x+y}b^{n-x-y} \\\\
= \sum_{k=0}^n \left\( \sum_{x+y=k, x\geq 0, y\geq 0} \binom{m}{x} \binom{n-m}{y}  \right) a^{k}b^{n-k}
$$

$x+y=k$ の組み合わせをまず計算してから、$k$ で $0 \sim n$ を足し合わせていくという形です。元々の左辺と右辺とを比較すると

$$
\begin{aligned}
\binom{n}{k}
&= \sum_{x+y=k, x\geq 0, y\geq 0} \binom{m}{x} \binom{n-m}{y} \\\\
&= \sum_{x=0}^k \binom{m}{x} \binom{n-m}{k-x} 
\end{aligned}
$$

両辺を $\binom{n}{k}$ で割ることで題意が示せました。


[^1]: この証明は一見「なぜそこの計算から出発するのか...」という気分になるので、流れだけでも抑えておいたほうがいいと思います。とりあえず「愚直にシグマ計算しても導出できない」くらいは覚えておければ時間を浪費することはないかと。