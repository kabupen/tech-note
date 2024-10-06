+++
title = 'ヤコビアン'
date = 2024-10-06T12:01:28+09:00
draft = true
categories = []
tags = ["統計"]
+++



# 

## 置換積分

一変数関数の積分に関する置換積分（変数変換）の公式について導入します。

$$
\int x\sqrt{1+x^2} dx
$$

この場合、

$$
t = 1+x^2
$$

という置換を行い

$$
dt = 2xdx \Leftrightarrow dx = \frac{dt}{2x}
$$

を用いることで

$$
\int x\sqrt{1+x^2} dx = \int x\sqrt{t} \frac{dt}{2x} = \dots
$$

と計算を進めることができます。



## ヤコビアン

多変数関数の変数変換の時には、ヤコビアンを用いて微小量を「拡大、縮小」する必要があります。

$$
x = x(u, v) \\\\
y = y(u, v)
$$

を用いた変数変換を行うと、

$$
\int \int f(x, y) dxdy = \int\int g(u, v) |J| dudv
$$

のように変換できます。ここで

$$
J = 
\det\begin{pmatrix}
\frac{\partial x}{\partial u} & \frac{\partial x}{\partial v} \\\\
\frac{\partial y}{\partial u} & \frac{\partial y}{\partial v}
\end{pmatrix}
$$

がヤコビアンと呼ばれる量で、$(x, y)$ 系における微小量を $(u, v)$ 系における微小量へ変換してくれる係数です。


### 微分の順序


ヤコビアンの計算に関する限りは、$x$ と $y$ のどちらを行とどちらを列にとるかは任意です。ただし、何を何で微分すべきかは抑えておく必要があります。


#### 覚え方①


$X$ の従う確率密度関数を $f_X(x)$ としたときに、$Y=g(X)$ の密度関数 $f_Y(y)$ は

$$
f_Y(y) = f_X(g^{-1}(y)) |\det J(\partial x/\partial y)|
$$

と表されます。$x=g^{-1}(y)$ なので

$$
f_Y(y) = f_X(x) |\partial x/\partial y|
$$

のように表しておくと、ヤコビアンの各成分の微分の方向（$\partial \rm{変換元}/\partial \rm{変換先}$）が頭に入りやすいと思います。


#### 覚え方②

ヤコビアンは

$$
dxdy = |J| dudv
$$

の係数であるので、これを変換すると

$$
|J| = \frac{dxdy}{dudv}
$$

となり、何を何で微分すべきかを思い出せると思います。