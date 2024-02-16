+++
title = 'You Only Need One Step: Fast Super-Resolution with Stable Diffusion via Scale Distillation'
date = 2024-02-16T00:54:54+09:00
draft = false
math = true
tags = ["Stable Diffusion"]
categories = ["arxiv"]
+++


# 論文情報

- You Only Need One Step: Fast Super-Resolution with Stable Diffusion via Scale Distillation

# Abstract

YONOS-SR という手法を導入し、単一のDDIMの過程を用いてSoTAの super-resolution の手法を導入した。Super-Resolution （SR）モデルは scale distillation（蒸留）を用いて学習している。直接 scale facotr を学習するのではなく（高解像度化に必要な倍率）、蒸留を用いて学習している[^あああ]。

[^あああ]: あああああ

```py
def test
```

`hoge`


# Introduction

拡散モデルでは denoising process に計算コストがかかってしまい、Stable Diffusion のような latent space で計算しているようなモデルでも推論速度は遅い。

高解像度化（super resolution; SR）タスクに用いられる場合だと64×64のパッチを扱うことが多いが、ニーズとしては 256×256 の画像を 1024×1024 の画像へ4倍にアップサンプリングするようなものが多く、16個のパッチに対して処理を行う必要がある。

通常の画像生成との違いは、SR では低解像度画像（low-resolution; LR）の情報を条件付として高解像度画像（high-resolution; HR）を作成することにある。text-to-image タスクと異なり、作成したい画像に関する条件付が強いような比較的シンプルなタスクとしての側面を持っている。

LR と HR の解像度の比率を scale factor と呼び、scale factor が小さいタスク（低解像度画像がある程度よい画質である）はより簡単なタスクとして位置づけられている。


# YONOS-SR

## Super resolution with latent diffusion models

### test
#### test
##### test


目的関数は

$$
{\rm{argmin}} E_{\epsilon, t} [\omega\_t(\lambda\_t) || \hat{z}\_\theta (z\_t, z\_l, \lambda_t) - z\_h ||_2^2
$$

で表される。

* $z_h$：high resolution の画像の latent vector
* $\hat{z}_\theta$：予測値
    * この予測は、前時刻、前時刻の low resolution の latent vector、signal-to-noise ratio に依存している 



## Scale distillation


SR タスクの学習のややこりいところとしては、scale factor がばらばらであるというところ。


![image](https://github.com/kabupen/papers/assets/19812756/15a76d9d-bcff-40a1-841f-1ffb58b74d70)



# Related Works

# 気になるワード
