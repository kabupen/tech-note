---
title: '今週の気になった情報たち vol.1'
description: ""
pubDate: 2024-03-01T00:21:14+09:00
heroImage: '@/assets/blog-placeholder-2.jpg'
tags: []
---
今週(?)の気になった論文などの情報をまとめておきます。適宜呼んだり情報を深追いしたりしていきます。

## 論文系

### Deep Networks Always Grok and Here is Why

- [Deep Networks Always Grok and Here is Why](https://arxiv.org/abs/2402.15555)
- https://www.slideshare.net/DeepLearningJP2016/dlgrokking-generalization-beyond-overfitting-on-small-algorithmic-datasets


ニューラルネットワークでは訓練誤差がゼロになった状態（過学習の状態）を超えて学習し続けると、急激な汎化性能の向上が見られる grokking（理解する）という現象が確認されています。本論文では grokking とは非線形領域（動画中の黒線）が分類面に移動する相転移がおき、サンプル周辺領域が線形化される（敵対的摂動にも頑健になる）現象がおこるという理由付けをしている点が面白そう。



### Binary Opacity Grids: Capturing Fine Geometric Detail for Mesh-Based View Synthesis

メッシューベースの3Dモデリングの新しい手法？？ NeRF や 3DGS との差異も気になるところです。


### Intriguing Properties of Diffusion Models: A Large-Scale Dataset for Evaluating Natural Attack Capability in Text-to-Image Generative Models

- https://arxiv.org/pdf/2308.15692.pdf

生成画像の「止まれ」の標識を誤認識する問題を深堀っていそうな論文。

### OOTDiffusion

- https://github.com/levihsu/OOTDiffusion

オンラインで人の画像に対して服装を合成できるようなモデル？


### GaussianShader: 3D Gaussian Splatting with Shading Functions for Reflective Surfaces

Gaussian Splat の派生版であるようなモデル？


## ツール系

### GLIGEN GUI

- https://github.com/mut-ex/gligen-gui

位置を bbox で指定しながら画像生成を行うことができるようなシステムです。ComfyUI をベースにしているものらしい。


### Stable Projectorz

- https://stableprojectorz.com/

Stable Diffusion web ui で使用できる、3Dレンダリングライブラリ

### Stable Diffusion 3