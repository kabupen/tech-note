+++
title = '自動微分について'
date = 2024-06-30
draft = false
math = true
categories = ["統計検定"]
tags = []
toc = false
+++



- 数値微分（numerical）



- 連鎖律（chain rule）
- 自動微分 
  - bottom up (forward mode)
  - top down (reverse mode)


### 数式微分

$f^\prime(x)$ を直接求める手法


### 自動微分


f(a) を計算すると同時に f'(a) の計算を行うためのアルゴリズム

$f^\prime(a)$ を直接求める手法


$R^n \to R^m$ 

で

- n << m なら bottom up
- n >> m なら top down



### 計算グラフ、DAG

## 問題設定


入力変数 $x_1, x_2$ に対して以下の関数を考えます。

$$
y = \ln x_1 + x_1x_2 - \sin x_2
$$

このときに、

$$
\left.\frac{\partial y}{\partial x_1} \right|_{x_1=a,~x_2=b}
$$

$$
\left.\frac{\partial y}{\partial x_2} \right|_{x_1=a,~x_2=b}
$$

の勾配を求めるような問題を考えます。以下では $x_1=2, x_2=5$ とします。



## 数式微分


まずこれまでの様に数式で導関数を算出し[^1]、そのあとに $x_1=2, x_2=5$ を代入して勾配を求める手法を採ります。この手法は数式微分（記号微分とも、symbolic differentiation）と呼ばれる手法です。

$$
\begin{aligned}
\frac{\partial y}{\partial x_1} &= \frac{1}{x_1} + x_2 \\\\
\frac{\partial y}{\partial x_2} &= x_1 - \cos x_2
\end{aligned}
$$

以上より、

$$
\left.\frac{\partial y}{\partial x_1}\right|_{x_1=2,~x_2=5} = 1/2 + 5 = 5.5
$$

$$
\left.\frac{\partial y}{\partial x_2}\right|_{x_1=2,~x_2=5} = 2 - \cos 5 = 1.716
$$

と求まります。


## 自動微分

以上の数式微分や数値微分をより効率化しようとして研究されているものが自動微分（auto differentiation）と呼ばれる手法です。この手法は forward mode (bottom up) と reverse mode (top down) と呼ばれる二種類の方法があります。 



### 連鎖律 （chain rule）


普段微分計算を行うときには、もはや chain rule を強く意識することはないと思います。











### Forward mode

1回の forward pass で、その変数 $x_1$ に対する出力変数の微分 $y_1, ..., y_m$ を求めることができる。これを入力変数分繰り返せば、$n$ 回でヤコビ行列を作成することができる。




### Reverse mode











## 参考文献

- https://huggingface.co/blog/andmholm/what-is-automatic-differentiation
http://www.kashi.info.waseda.ac.jp/~kashi/lec2023/nad/krawczyk.pdf

http://www.kashi.info.waseda.ac.jp/~kashi/lec2021/nad/autodif-slide-j.pdf





[^1]: 「これまでの」とは人によって定義がかなり異なるとは思いますが、紙とペンで微分計算を行っていたあの頃の延長線を考えます。