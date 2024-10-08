+++
title = '確率変数の和の分布'
date = 2024-05-11
draft = false
math = true
categories = ["統計検定"]
tags = []
toc = false
+++



確率変数の変数変換に伴う変換公式について理解し、その応用としての和の分布を求めるための畳み込み法について紹介します。

## 問題設定

$X, Y$ を確率変数としたときに

$$
S = g_1 (X, Y) \\\\
T = g_2 (X, Y)
$$

となる変数変換を考えます。このとき $(X, Y)$ の同時確率密度関数が $f_{X,Y}(x, y)$ である場合に、$(S, T)$ の同時確率密度関数を求めます。


### 何が難しいか

そもそも $(S,T)$ の同時確率密度関数の形が分からないため

$$
f_{S,T}(s, t)
$$

という関数としては表すことができても、実際の関数の形を書き下すことはできないです。そもそも何も分からないという点がはじめに難しい点です。

次に、変数変換の式を $(X, Y)$ に関して解くと

$$
X = h_1 (S, T) \\\\
Y = h_2 (S, T)
$$

というように表現できます。これを用いると

$$
f_{X, Y}(x, y) = f_{X, Y}(h_1(s, t), h_2(s, t))
$$

という変形ができますが、$(S, T)$ を含むように変形はできたものの、これが何を意味しているのかも不明でよくわからないというのが２つ目の難しい点であると感じます[^2]。

以上から、確率変数の変数変換はなんとなく一筋縄ではいきそうにはないという雰囲気を感じ取っていただければと思います。




## 重積分の変数変換

ではどのように考えるのかというと、確率密度関数の積分に注目して考えていきます。確率変数 $(X, Y)$ の $(x, y) \in D$ における確率を表すと

$$
P( (X, Y) \in D) = \iint_{(x,y)\in D} f_{X, Y}(x, y) dxdy
$$

となります。ここで $f_{X,Y}(x,y)$ は同時確率密度関数です。重積分の変数変換の公式を用いることで

$$
P( (X, Y) \in D) = \iint_{(x,y)\in D} f_{X, Y}(x, y) dxdy = \iint_{(s,t)\in C} f_{X, Y}(h_1(s,t), h_2(s, t)) |J| dsdt
$$

と変形することができ、この式は $P((S,T)\in C)$ を表しているに他なりません。ということで、確率変数 $(S,T)$ の同時確率密度関数は

$$
f_{X, Y}(h_1(s,t), h_2(s, t)) |J| 
$$

で表すことができました。$|J|$ はヤコビ行列の行列式の絶対値です。

確率変数の変数変換を行いたいのに、ふと気づくと重積分の変数変換の公式が出てくることになっているのですが、これは確率密度関数の積分式を用いたいからです。


### ヤコビ行列・ヤコビアン

ところで、$J$ はヤコビ行列とよばれるもので

$$
J = 
\begin{pmatrix}
\cfrac{\partial x}{\partial u} & \cfrac{\partial x}{\partial v} \\\\
\cfrac{\partial y}{\partial u} & \cfrac{\partial y}{\partial v} \\\\
\end{pmatrix}
$$

で定義されます。この行列式 $J$ がヤコビアンと呼ばれます[^1]。 
重積分における変数変換では

$$
x = x(u, v) = \alpha u + \beta v \\\\
y = y(u, v) = \gamma u + \epsilon v
$$

という積分変数の変数変換に加えて

$$
dxdy \to dudv
$$

という積分要素の変換も必要となります。そのときの変換係数がヤコビアンで

$$
dxdy = |J| dudv
$$

という関係式で変換することができるようになります。




[^1]: ヤコビ行列の行列式がヤコビアン $J$ であり、変数変換に使用しているのはヤコビアンの絶対値を取った値 $|J|$ であることに留意して下さい。
[^2]: 同じ $f$ という関数名を使用していますが、$f_{X, Y}$ と $f_{S, T}$ は意味が異なっているということを思い出しておいて下さい。