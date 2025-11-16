+++
title = '255d7d9044e08d'
date = 2025-05-24T08:49:33+09:00
draft = false
categories = []
tags = []
+++

# 数学的準備

## ベクトル


### 位置ベクトル

原点から点$A$ に向かうベクトルを位置ベクトルといい

$$
\vec{OA} = (x_1, y_1, z_1)
$$

と表し、原点からの変位としてベクトルを定義したものです。
また、$A$ から $B$ に向かうベクトルは

$$
\vec{B} - \vec{A}
$$

ベクトルです。


### スカラー場


スカラー場は空間の各点にスカラー量を対応させる関数であり、

$$
V(\vec{r}) = k \frac{q}{|\vec{r}|}
$$

の静電ポテンシャルのように、位置を指定するとスカラー値が返ってくる関数です。
ベクトル場は空間の各点にベクトル量を対応させる関数であり、


### ベクトル場

空間の1点 $(x_0, y_0, z_0)$ を決めると、ベクトルが以下のように計算される：

$$
\vec{V}(x_0, y_0, z_0) = \left( V_1(x_0, y_0, z_0),\ V_2(x_0, y_0, z_0),\ V_3(x_0, y_0, z_0) \right)
$$

得られたベクトルは、**指定した空間の点を始点** としたベクトルであることに留意。

$$
\vec{E}(r) = k \frac{q}{|r|^3} \vec{r}
$$

の電場のように、位置を指定するとベクトル値が返ってくる関数です。


## 面積分

### ベクトル場の面積分

ある面をベクトル場がどれだけ突き抜けるかを定量化する計算で、

$$
\iint_S \vec{F}(x) \cdot \vec{n}(x) dS
$$

と表されます。ここで

- $\vec{n}$ は面の単位法線ベクトル
- $dS$ は微小面積

を表しています。そのため、ベクトル場が着目している面に垂直な成分をどれだけ持っているかを表現する計算になっています。


## 勾配、発散、回転

### 勾配

スカラー場 $\phi(x, y, z)$ が与えられたとき、これから定義されるベクトル

$$
{\rm{grad}} \phi(x, y, z) = \left(\frac{\partial \phi}{\partial x},\frac{\partial \phi}{\partial y},\frac{\partial \phi}{\partial z}\right)
$$

を gradient（勾配）といいます。

### 発散

ベクトル場 $\bold{A}$ が与えられたとき、

$$
{\rm{div}} \bold{A}(x, y, z) = \frac{\partial A}{\partial x} + \frac{\partial A}{\partial y} + \frac{\partial A}{\partial z}
$$

を divergnce（発散）という。

一般的には閉曲面外向きに法線ベクトル正の向きを取るので

- 正の発散 $\nabla A > 0$ は小領域から「流れ出す」
- 負の発散 $\nabla A < 0$ は小領域から「流れ込む」

となる。

### 回転

$$
{\rm{rot}} \bold{A}(x, y, z) = \left(
    \frac{\partial A_z}{\partial y} - \frac{\partial A_y}{\partial z},~
    \frac{\partial A_x}{\partial z} - \frac{\partial A_z}{\partial x},~
    \frac{\partial A_y}{\partial x} - \frac{\partial A_x}{\partial y}
    \right)
$$

を rotatoin（回転）といいます。


- https://www2.math.kyushu-u.ac.jp/~hara/lectures/05/zoku-text050627.pdf



## 立体角

ラジアンの定義は

$$
\theta = \frac{\ell}{r}
$$

で与えられ、半径に対する弧の長さの比で定義されます。

ステラジアン（立体角）の定義は

$$
\Omega = \frac{S}{r^2}
$$

で与えられ、半径の二乗に対する面積の比で定義されます。



## ガウスの定理

$$
\int_V (\nabla \cdot \mathbf{A}) ~dV = \oint_S \mathbf{A} \cdot d\mathbf{S}
$$

- V：体積領域
- S：その体積を囲む閉曲面
  - イメージは単なる曲面ではなく、球面のように "閉じた" 表面であることに留意

## ストークスの定理


$$
\oint_{C} \mathbf{A} \cdot d\mathbf{l} = \int_{S} (\nabla \times \mathbf{A}) \cdot d\mathbf{S}
$$


- 左辺：曲線 C に沿ってベクトル場 A を周回線積分したもの
- 右辺：その曲線 C を縁とする任意の曲面 S 上で、 A の回転を面積分したもの

直感的なイメージは、輪の周りの流れをすべて合計すると（左辺）、輪の内部の渦の合計（右辺）に等しいというもので、
輪の内部の合計はうまく方向が打ち消し合うので結局輪の外周だけの成分が残るというもの。


# 力学的準備


## 仕事

運動方程式を用いることで物体の運動を記述できるが、実際にはさまざまな観点から詳細な解析が難しいことがある。
エネルギーの概念、保存則の導入により、運動を理解するための非常に強力なツールを手にすることができる。

仕事 $W$ は次で定義される。

$$
\vec{W} = \int_{x_1}^{x_2} F(x) dx
$$

仕事の単位は

$$
[\text{仕事}] = \mathrm{N \cdot m} = \mathrm{kg \cdot m^2 / s^2} = \mathrm{J} \quad \text{（ジュール）}
$$

エネルギーの単位に等しく、仕事をする能力をもつときエネルギーをもつという（持っているエネルギー分だけ仕事できる）。


### 仕事エネルギー定理

運動方程式から出発することで

$$
\begin{align*}
F &= m \frac{dv}{dt} \\\\
v \cdot F &= \frac{d}{dt} \left( \frac{1}{2} mv^2 \right) \\\\
\int_{t_1}^{t_2} F \frac{dx}{dt} dt &=  \int_{t_1}^{t_2} \frac{d}{dt} \left( \frac{1}{2} mv^2 \right) dt \\\\
\int_{t_1}^{t_2} F dx &= K_2 - K_1 
\end{align*}
$$

外力によってなされた仕事はエネルギーの変化に等しいことを示せる。


### 単位

- 力の単位は「N」（ニュートン）
- エネルギーの単位は「J」（ジュール）


## ポテンシャル / ポテンシャルエネルギー

保存力であれば

$$
\oint_C \vec{F} \cdot d\vec{r} = 0
$$

閉回路についての線積分についてゼロになる。