+++
title = 'DoRA: Weight-Decomposed Low-Rank Adaptation'
date = 2024-02-19T14:18:49+09:00
draft = true
math = true
tags = []
categories = []
toc = true
+++


## Introduction

Full fine tuning（FT）は近年の大規模モデルではその計算コストの大きさが問題となってきています。そこで parameter-efficient fine-tuning（PEFT）と括られるような fine-tuning 手法が発展してきており、LoRA などもその手法の一種です。LoRA ではモデル構造を変えることなく少ないパラメータ数にもかかわらず高精度な fine-tuning が可能な手法で、様々な派生手法が発展しています。

ただし FT と PEFT の精度には依然として差があるのも事実です。そこで本論文ではそれらの差を測るための docompose 手法を導入し、Weight-Decomposed Low-Rank Adaption（DoRA）と呼ばれる学習方法を用いることで精度改善を実現しています。decompose の方法が Figure.1 で示されています。


{{< figure src="20240219-152119.png" width="500" >}} 


## Pattern Analysis of LoRA and FT

### Low-Rank Adaption (LoRA)

LoRA は事前学習済モデルに対する adaptor として fine-tunig を実現する手法で、元モデルの重み $W_0 \in R^{d\times k}$ に対して、$B\in R^{d\times r}, A\in R^{r\times d}$ の低ランク行列を用いて

$$
W^\prime = W_0 + \Delta W = W_0 + BA
$$

fine-tuning による更新 $\Delta W$ をこれらの積で置き換える方法です。行列のランク $r$ を大きくしていくことで FT になることから、LoRA は FT の近似手法として捉えることができます。

ただしなぜ近似できるかについては依然として研究中というところでしょうか。

> Building upon the hypothesis that updates made during the fine-tuning exhibit a low “intrinsic rank”,

本論文では以上のように LoRA を引いているのですが、LoRA はあくまでも "intrinsic rank"（固有ランク）の存在を "仮定" している手法です。完全な $d$ 次元空間での最適化ではなく $r$ 次元部分空間での最適化で十分だと報告しています。現にその通りに LoRA の精度は非常に良いのですが、理論的裏付けはまだまだ発展段階です。そのため本論文でも「LoRA と FT の違いとは何か？」から議論を出発させています。

### Weight decomposition Analysis


本論文では先行研究である [weight normalization](https://arxiv.org/abs/1602.07868) のアイデアを受けて、重み行列を以下のように分解することで、LoRA と FT との性能比較を行っていきます。重み行列を $W \in R^{d\times k}$ としたときに

$$
W = m \frac{V}{||V||_c}
$$

と分解します。$m$ は $1\times k$ の magnitude vector、$V$ は $d\times k$ の directional matrix です。また $||V||_c$ は各行のベクトルに対する正規化係数です。行列で見ると少しややこしいですが、$W$ の各行ベクトル $w$ に対してみてみると

$$
w = g \frac{v}{||v||}
$$

の様に、$v/||v||$ の（方向）ベクトルと、係数 $g$ に分解しているだけです。これを行列にまとめ見たのが上式です。このように分解することで重みの "大きさ" と "方向" とを定量化することができ、これらの量を以て FT との比較を行います。

### Analysis Results

LoRA と FT に関して、それぞれの事前学習済モデルとの magnitude と direction の違いを見たのが Figure.2 (a)(b) です。

{{< figure src="20240219-144525.png" width="600" >}} 

面白いことに $\Delta M$ と $\Delta D$ との相関が正負逆転していることが見て取れます。この差分を埋めることができないか？というのが本論文での提案手法である DoRA の背景です。


## Method

### Weight-Decomposed Low-Rank Adaptation


DoRA では以下の更新式に従って学習を行います。

$$
W^\prime = m\frac{W_0 + BA}{||W_0 + BA||_c}
$$

これにより先程見た $\Delta M, \Delta D$ の関係図は

{{< figure src="20240219-150739.png" width="700" >}} 

のように、FT と DoRA の相関が同じになりました。



## Experiments

いくつかの実験結果を確認します。Table. 1 では、その他の fine-tunig 手法と、DoRA をh疑核し、精度を上回っていることが確認できます。

{{< figure src="20240219-151045.png" width="700" >}} 



## Summary

本論文をまとめておきます。

- LoRA で提案されている低ランク行列近似を発展させた手法
- 重みの更新を大きさと方向に分割しており、それによって学習の性質が FT と近しいものになった
  - 分割によって方向に関する更新が stable になった

