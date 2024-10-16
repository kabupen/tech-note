+++
title = 'マルコフの不等式・チェビシェフの不等式'
date = 2024-10-16T09:59:36+09:00
draft = true
categories = []
tags = ["統計"]
+++


## マルコフの不等式

確率変数 $X$ について、
$$
P(|X| \leq c) \leq \frac{E[|X|]}{c}
$$
が成り立ち、これをマルコフの不等式と呼びます。


### 証明

$X$ の値の範囲を条件に持つような2種類の定義関数を導入します。
$$
I(|X| \geq c) = 
\begin{equation*}
   \begin{cases}
      1~~(|X| \geq c) \\\\
      0~~(|X| < c) \\\\
   \end{cases}
\end{equation*}
$$
$$
I(|X| < c) = 
\begin{equation*}
   \begin{cases}
      1~~(|X| < c) \\\\
      0~~(|X| \geq c) \\\\
   \end{cases}
\end{equation*}
$$
これらは互いに排他的な関係性にあるため、同時に $1$ にはならず
$$
I(|X| \geq c) + I(|X| < c) = 1
$$
の関係式となります。これを用いて
$$
\begin{aligned}
E[|X|] 
&= E[|X| \left\(I(|X| \geq c) + I(|X| < c) \right\)] \\\\
&\geq E[|X| I(|X| \geq c)] \\\\
&\geq c \cdot E[I(|X| \geq c)] \\\\
&= c \cdot P(|X| \geq c) \\\\
\therefore
\frac{E[|X|]}{c} &\geq \cdot P(|X| \geq c)  \\\\
\end{aligned}
$$


### チェビシェフの不等式

マルコフの不等式において
$$
X \to (X-\mu)^2,~~ c \to k^2
$$
の置き換えを行うと、以下の不等式が成り立ちます。
$$
P(|X-\mu| \leq k) \leq \frac{\sigma^2}{k^2}
$$


## 直感的なイメージ

マルコフの不等式、チェビシェフの不等式の直感的なイメージについて調べてみたいと思います。マルコフの不等式は
$$
P(|X| \leq c) \leq \frac{E[|X|]}{c}
$$
であり、左辺は確率変数がある値（しきい値）$c$ を超える確率を意味していて、その確率に上限をつけることができるというものです。

### 例

ある銀行に預けている預金の平均残高が10万円だとします。今、預金残高が100万円以上の人がどのくらいいるかを知りたいとします。
マルコフの不等式を使うと、次のように計算できます。
$$
P(|X| \leq 100) \leq \frac{E[|X|]}{100} = \frac{10}{100} = 0.1
$$
したがって、預金残高が100万円以上の人は最大でも10％ しかいないことがわかります。この「最大でも」というのがミソであり、実際はこの街には100万円以上の預金を持っている人はゼロかもしれませんし、0.1% はいるかもしれません。具体的な確率はわからないものの、上限値を設定できるというのがマルコフの不等式です[^1]。

### もう少し踏み込んで

先程の例は具体的な数値を用いた計算でしたが、少し抽象化すると次のように理解できます。とある確率分布に従う確率変数 $X$ に対して、元の確率分布の性質は全くわからないが、期待値 $E[X]$ だけ分かっているものとします。この場合に、確率変数 $X$ が期待値の10倍の大きさを持つ値となる確率は
$$
P(|X| \leq 10\cdot E[X]) \leq \frac{E[|X|]}{10 \cdot E[X]} = 0.1 
$$
となることが分かり、期待値から大きくハズレた値を取る確率は小さくなってくる、という直感的なイメージと合う結論が導けます。




[^1]: 従う確率分布が分からないのに、期待値（平均）が計算できるというのは現実的ではないなと思います。実際には標本平均を用いたりと（大数の法則からサンプル数が多い場合には、母平均に確率収束するため）、よりざっくりとした関係式になってくると思います。