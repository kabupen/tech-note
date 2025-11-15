+++
title = '1-1 質点の力学'
date = 2025-10-31T07:57:04+09:00
draft = false
+++

## §1.1 質点の力学

### 力のモーメント（トルク）


力のモーメントもしくはトルクを
$$
N = r \times F
$$
で定義します。
一次元であれば $N=rF\sin\theta$ で表される量で、ある点 $O$ 周りで「どれだけ回そうとしているか」を表します。
並進運動については単に力 $F$ で「どれだけ動かそうとしているか」を表せるのに対して、回転運動はどんな力 $F$ で、どこ $r$ に作用させるかが重要となっています。
トルクの単位は
$$
\rm{m} \cdot \rm{kg} \rm{m/s^2} 
$$
です。


### 角運動量

角運動量を
$$
L = r \times p
$$
で定義します。時間微分を考えると
$$
\frac{d}{dt} = v\times p + r \times m \frac{d}{dt}p = r \times F = N
$$
となり、角運動量の時間変化がトルクになることが分かります。
そのため時間あたりの角運動量が、物体をどれくらい回転させようとしているか（=トルク）という意味を持つことになります。


### ポテンシャルエネルギー

準備として、ストークスの定理について定義します。
ベクトル場 $F$ の回転（curl）は
$$
\nabla \times \vec{F} =
\begin{pmatrix}
\frac{\partial F_z}{\partial y} - \frac{\partial F_y}{\partial z} \\\\
\frac{\partial F_x}{\partial z} - \frac{\partial F_z}{\partial x} \\\\
\frac{\partial F_y}{\partial x} - \frac{\partial F_x}{\partial y}
\end{pmatrix}
$$
で計算でき、「どの軸のまわりにいちばん強く回ろうとしているか」を表す回転軸の向きです。例えば2次元の渦を考えると $z$ 成分がゼロであるので
$$
\nabla \times \vec{F} =
\begin{pmatrix}
0 \\\\
0 \\\\
\frac{\partial F_y}{\partial x} - \frac{\partial F_x}{\partial y}
\end{pmatrix}
$$
となり、$z$ 軸方向のベクトルを持つことが分かります。渦の回転軸が2次元平面と直行した$z$軸方向にあることと直感的に一致します。
このように回転は「回転軸とその方向」を計算する演算の意味を持ちます。一般的に、位置 $r_0$ での回転軸の方向を表現すると言えます。

ストークスの定理は
$$
\oint_C \vec{F} \cdot d\vec{r} = \iint_S (\nabla \times \vec{F}) \cdot \vec{n}\\, dS
$$