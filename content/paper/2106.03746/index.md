+++
title = 'Efficient Training of Visual Transformers with Small Datasets'
date = 2024-03-05T19:28:32+09:00
draft = true
math = true
tags = []
categories = []
toc = true
+++


## Introduction

Visual Transformer（VTs）[^1]は従来画像処理で使用されていた CNN とは異なった構造を持っているモデルであり、様々なタスクで成功を収めています。VTs ではパッチ分割しそれらを embedding し、トークンとして扱うことで、自然言語タスクで用いられている Transformer を画像処理にも応用することを可能にしています。

VTs の大きな強みの一つは attention layer を用いることで、画像の大局的な関係性（global relations between tokens）を獲得しモデル内で特徴量として使用できる点です。この点は CNN が receptive field がカーネルサイズに制限されるため、局所的な情報、回転不変性、階層構造の情報を使用して inductive bias（帰納バイアス）を獲得している点と異なっています。そのため VTs の学習では大量のデータが必要とされています。

例えば Vision Transformer（ViT）では

{{< figure src="./20240305-195530.png" width="600" >}} 

パッチ分割の方法が overlap を持っておらず、global relations の獲得が得意な反面、局所的な関係性を計算することが困難でした。

これらの問題を解決するために、第２世代の VTs では畳み込み層と attention layer を混ぜたようなモデルアーキテクチャが提案されています。こうすることで VT に局所的な帰納バイアスを組み込んでいます。Swin Transformers では

{{< figure src="./20240305-195841.png" width="500" >}}

パッチ分割方法を工夫することで、この課題解決に取り組んでいます。



## VT の構造について

典型的な第２世代の VTs のアーキテクチャが Figure.1 (a) で示されています。画像はパッチ分割され $K \times K$ の情報になった後に、畳み込みなどを用いることで $k \times k$ サイズに削減され（$k<K$）、それらの情報を用いて downstream のタスクを解きます。

{{< figure src="./20240305-200653.png" width="700" >}}


### Dense relative localization task

本論文では VTs の特性理解に加えて、dense relative localization loss を導入することで局所的な情報を明示的に取り入れる効果についても論じています。Figure.1 (b) でもあるように、パッチペアを取得しそれらの相対的な距離（縦方向、横方向）を予測するタスクを解かせます。このタスクだけを解かせるのではなく、学習時には

$$
L_{ce} + \lambda L_{drloc}
$$

の形式で重み付けした上で全体の損失関数を最適化していきます。


もう少し平たく理解すると、$L_{drloc}$ を最適化するタスクは帰納バイアス（inductive bias）を獲得するためのタスクであると言えます。パッチ間の空間情報（位置関係）を明示的に取り入れることができます。


## Experiments


使用したデータセットは以下のとおりです。VTs が通常学習に使用しているデータセットのサイズと比較すると、中程度から小規模なデータセットを用意しています。

{{< figure src="./20240305-202141.png" width=400 >}}



### Trained from scratch

100 epoch でスクラッチから学習をしてみた結果が Table. 4です。


{{< figure src="./20240305-202340.png" width=400 >}}

ここから読み取れることは次の様な事項です：

- VTs は medium dataset で学習した場合は、ResNet-50 と比較して精度が悪い傾向にある
- CvT がその他の VTs よりも平均的によい精度を持っていること
  - 帰納バイアス（inductive bias）を取り込んでいるアーキテクチャかどうかの差異
- $L_{drloc}$ をいれることで、VTs は精度が大幅に改善する
  - 帰納バイアス（inductive bias）の有無はやはり重要である
  - REhesNet-50 では大きな改善はなかったことからも、アーキテクチャとして bias を持っているかどうかが一つのポイントであると言える



## Conclusion


本論文では小中規模のデータセットで訓練された異なる VTs の性能が大きく異なることを見てきました。CvT は少ないデータでより効果的に一般化することができことから、medium size のデータセットでの学習時には帰納バイアスの有無が性能に関わっていることが示唆されています。

ただし本論文では主にResNet-50と同等サイズのVTに焦点を当てており、データの少ないシナリオでは高容量モデルが最適でない可能性が示唆されているが、その点は将来的な研究課題であるそうです。


[^1]: ここでは Vision Transformer (ViT) 以外のモデルについて議論しているため、"Visual" Transformer という表現になっています。