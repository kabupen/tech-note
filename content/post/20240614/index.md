+++
title = 'NeRF の基本'
date = 2024-06-14
draft = false
math = true
categories = ["NeRF"]
tags = []
toc = false
+++


NeRF について理論背景から抑えていきたいと思います。


# レンダリング方程式


## Transmittance function


transmittance function \\( T(t) \\) を、粒子が \\( \[0, t) \\) の間に（\\(t\\) の単位は [m] です）散逸しない確率として定義します。つまり粒子がまっすぐどこにも散乱せず距離 \\(t\\) を進む確率です。ここである地点からある地点まで散逸しない確率

$$
T(a\to b)
$$

を求めてみます。

ここで \\(\sigma(t)\\) を differential likelihood とします。光線が微小距離 \\(dt\\) だけ進む際に散逸する確率を表します。\\(\sigma(t)\\) を図に表すと以下のようになり

{{< figure src="figure1.png" width=100 >}}

光線の進む先にある物質などの性質によって「ここでは散逸しやすい」「ここでは透過しやすい」などを表現することができます。



$x$


# Volume Rendering




# 参考文献

- https://arxiv.org/abs/2209.02417

