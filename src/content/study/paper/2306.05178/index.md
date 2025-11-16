+++
title = 'SyncDiffusion: Coherent Montage via Synchronized Joint Diffusions'
date = 2024-01-25
draft = false
math = true
tags = ["Stable Diffusion"]
categories = ["arxiv"]
toc = false
+++


- [SyncDiffusion: Coherent Montage via Synchronized Joint Diffusions](https://arxiv.org/abs/2306.05178)

# Abstract

パノラマ画像を生成する際に既存の Diffusion model ではモンタージュするのには限界があったのですが、本論文では SyncDiffusion と呼ばれるモデルを提案して従来手法の限界を更新しています。

# Related work

## Few-shot/Zero-shot adaptation

StableDiffusion を再学習せず条件づけする技術として

- ControlNet
- Custom Diffusion
- SDEdit
- RePaint
- Guided diffusion

などがあげられています。本研究では guided diffusion framework を導入しています。


## Mantage Generation

MultiDiffusion, DiffCollage では各 reverse step において中間生成物を結合してパノラマ画像を作成していたため、画像全体の一貫性（global semantic coherence）の保持は難しかったようです。


## DDPM

Denoising Diffusion Probabilistic Models ではデータ分布 $q(x_0)$ を $p_\theta(x_0)$ で近似する手法を採っています。時刻 $t$ でガウスノイズからサンプリングして、それを逆拡散することでデータを生成します：

![image](https://github.com/kabupen/papers/assets/19812756/908fedf9-42fb-45c6-91b4-4acc86999d97)



## Joint Diffusion

MultiDiffusion では multi-window joint diffusion approach を採ることでパノラマ画像を生成しています。パノラマ全体の画像を、各ウィンドウ（パッチ）に対応した情報で正規化している？

$$
z_{t} = \frac{ \sum_{i} T_{i \rightarrow z}(x_{t}^{(i)})}{\Sigma m^{(i)}}
$$




# SyncDiffusion

MultiDiffusion では全体の統一感がなくなる画像が生成されてしまいます：

![image](https://github.com/kabupen/papers/assets/19812756/38110784-39e7-4466-8301-830b99971f7c)

同様に SyncDiffusion でも reverse process におけるノイズ画像を更新する。重なっている領域の色味や latent features を平均化するのではなく、perceptual similarity loss の back prop. を利用している（？）。

## perceptual similarity loss

LPIPS, Style Loss と呼ばれる off-the-shelf loss function を使用して、画像の "スタイル" に関する loss を計算しています。各パッチごとの類似性を計算して、似通うように計算することで overlap 部分や画像全体の一貫性を担保しています。

![image](https://github.com/kabupen/papers/assets/19812756/e1339999-3931-4c9a-8ab3-7d57dc796b1f)

- noise の状態だと似たような loss の値
- 最終的に生成する $x_0$ に対して loss は似ていれば小さく、離れていれば大きくなる

## 疑似アルゴリズム

- ある $i$ 番目のパッチの画像生成方法
- anchor window （画風を固定するための参考情報として使用する window）との loss を計算して行って、その loss を使って latent imates ($x$) を修正していく


![image](https://github.com/kabupen/papers/assets/19812756/5d5cd4e9-9bd8-4c7c-82d2-c47d4fefe0ee)



## Applications

layout-to-image pipeline で使用した場合、従来手法よりも画像全体の一貫性は担保できていることが分かります（背景の天気の具合）：

![image](https://github.com/kabupen/papers/assets/19812756/fa74724c-8a29-43da-bc05-b47cd09c5383)

 





## 気になるキーワード

- MultiDiffusion: Fusing Diffusion Paths for Controlled Image Generation
- DiffCollage: Parallel Generation of Large Content with Diffusion Models
- LPIPS（Learned Perceptual Image Patch Similarity）