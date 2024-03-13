+++
title = '半教師あり学習'
date = 2024-03-06T19:42:59+09:00
draft = true
math = true
categories = []
tags = []
toc = true
+++


## 学習方法について


半教師あり学習について、[A Survey on Deep Semi-supervised Learning](https://arxiv.org/abs/2103.00550) を参考にまとめます。ネットワークの学習手法について主に３つの手法があります。

- 教師あり学習 (Supervied Learning; SL)
  - ラベル付きデータを用いて学習を行う手法
- 半教師あり学習 (Semi-Supervied Learning; SSL)
  - 小量のラベル付きデータと、ラベル無しデータとを使用して学習を行う手法
- 自己教師あり学習 (Self-Supervied Learning; SSL)
  - ラベル無しデータのみを使用して学習を行う手法

本ブログでは半教師あり学習について着目するのですが、以下の図の様に大きくわけて５つの手法があります。このうち Pseudo-labeling methods と Hybrid method についてまとめます[^4]。

{{< figure src="./20240313-1132.png" width=800 >}}





## Pseudo-labeling methods

ラベル無しデータに対して pseudo label（疑似ラベル）を割り当てていく手法の総称が pseudo-labeling methods です。Pseudo labele の[初出の論文](https://citeseerx.ist.psu.edu/document?repid=rep1&type=pdf&doi=798d9840d2439a0e5d47bcf5d164aa46d5e7dc26)では学習中のモデルの出力の信頼度が高いものが真のラベルであるとして損失を計算する手法を提案していました。これと比較して、蒸留などで用いられる手法では学習済みモデルの出力を用いてラベルを割り当てる方法が提案されています。そのため一口に「疑似ラベル」と言ってもその割り振り方法は様々に工夫のしがいがある部分であるので、どの手法を指しているかは文脈判断する必要があります。


### Disagreement-based models

一つのタスクに対して複数のモデルを学習し、それらの情報を相互に使用することでラベル無しデータを扱っていく手法です。この手法の一つである、Co-training（共学習）について以下で詳しく見てきます。


#### 具体例

RGB-D Object Recognition の2016年の[論文](https://www.ijcai.org/Proceedings/16/Papers/473.pdf)を例に、disagreement-based models について説明していきます。
この研究ではRGB-D 情報を用いた物体検知において、半教師あり学習を用いた手法を導入することでアノテーションコストを下げつつニューラルネットワークの学習を可能としました[^1]。


{{< figure src="./20240313-003206.png" width=700 >}}

まず学習初期ではラベル付きデータを用いて、それぞれ RGB 情報**のみ**からタスクを解くモデル（RGBモデル）、Depth情報**のみ**からタスクを解くモデル（Depthモデル）を学習させます。ここでのタスクとは、例えば画像の物体のクラス分類などを念頭に置いています。

次にこれらのモデルを用いて、ラベル無しデータに対して pseudo labeling を行っていきます。RGB情報のみから分類した結果、Depth情報のみから分類した結果を信頼度でランキングするのですが、同じ画像に対してもそれぞれのモデルの "癖" があるために同じ出力結果にはならないことが予想できます。RGBモデルで擬似ラベルを作成したデータは次のDepthモデルの学習データに、Depthモデルで擬似ラベルを作成したデータは次のRGBモデルの学習データとします。この様にすることで、RGBモデルの不得手とする画像を効果的に学習させることができ、Depthモデルについても同様の状況になります。上図で prediction　から labeled data へ移動する際に、RGBモデルの出力がDepthモデルへ、Depthモデルの出力がRGBモデルへ入力されていることに留意して見てみて下さい。

つまり Disagreement-based models の肝は、データの別の異なる特性に着目したモデルを用いることにあります。１つのモデルを用いるのではなくデータの特性にそれぞれ特化したモデルを用いることで、過学習の抑制にも繋がり汎化性能を期待できます [^2]。


#### Summary


RGB-D Object Recognition を例に Diagreement-based models を説明しました。Disagreement とは例のように、２つのモデル出力の不一致（disagreement）を利用して pseudo labeling を行っているのでそのように呼ばれます。




### Self-training models　（自己学習モデル）


Self-training models は、モデル自分自身の予測値を用いて疑似ラベルを割り当てていく手法です。



#### Enrotpy Minimization

Entropy Minimization は [[Yves et. al, 2004]](https://proceedings.neurips.cc/paper_files/paper/2004/file/96f2b50b5d3613adf9c27049b2a888c7-Paper.pdf) で提案された手法で、モデルの予測値のばらつき（entorpy）を抑える様に学習を進めます。


#### Pseudo Label

Pseudo-Label は [[D.-H. Lee, 2013]](https://citeseerx.ist.psu.edu/document?repid=rep1&type=pdf&doi=798d9840d2439a0e5d47bcf5d164aa46d5e7dc26) で提案された手法で、疑似ラベルを割り当てていくという手法の初出のものです。損失関数は以下で定義されます：

$$
L = \frac{1}{n} \sum_{m=1}^n \sum_{i=1}^K R(y_i^m, f_i^m) + \alpha(t) \frac{1}{n^\prime} \sum_{m=1}^{n^\prime} \sum_{i=1}^K R({y_i^\prime}^m, {f_i^\prime}^m)
$$

第一項はラベル付きデータに対する損失関数で、これは従来のクラス分類の損失関数を用いています。第二項はラベルなしデータに対する損失関数で、モデルの出力 ${f_i^\prime}^m$ のうち最も信頼度（confidence）の高いラベルを真値 ${y^\prime}^m$ として同様のクラス分類用の損失関数を計算しています[^3]。






#### Noisy Student


Noisy Student は [[Q. Xie et. al, 2020]](https://arxiv.org/pdf/1911.04252.pdf) で提案された手法で、基本的には知識蒸留（knowledge distillation）に沿った手法です。差異は、生徒モデル学習時に noise（データ拡張; Data Augmentation）を使用することと、教師モデルよりも大きなパラメーターを持つ生徒モデルを使用する点にあります。









#### S4L










#### Meta Pseudo Labels （MPL）


Meta Pseudo Labels（MPL）は [[H. Pham et. al, 2020]](https://arxiv.org/abs/2003.10580) で提案された手法で、従来の知識蒸留（下図；左）の手法を更新し、生徒モデル（下図；右）からのフィードバックを教師モデルが受けるという手法です。

{{< figure src="./20240313-111914.png" width=600 >}}





### Hybrid

上記２つの手法を取り入れたものとして、MixMatch、FixMatch などが挙げられます。



## 参考情報

1. [A Survey on Deep Semi-supervised Learning](https://arxiv.org/abs/2103.00550)
1. [Pseudo-Label:The Simple and Efficient Semi-Supervised Learning Method for Deep Neural Networks](https://citeseerx.ist.psu.edu/document?repid=rep1&type=pdf&doi=798d9840d2439a0e5d47bcf5d164aa46d5e7dc26)
2. [Semi-Supervised Multimodal Deep Learning for RGB-D Object Recognition](https://www.ijcai.org/Proceedings/16/Papers/473.pdf)
3. [Semi-supervised Learning by Entropy Minimization](https://proceedings.neurips.cc/paper_files/paper/2004/file/96f2b50b5d3613adf9c27049b2a888c7-Paper.pdf)
4. [画像分類タスクにおける半教師有り学習 第1回](https://techblog.morphoinc.com/entry/2020/12/25/113050)


[^1]: ImageNet のような大規模データセットがないため、半教師あり学習を用いてこの問題に対処しているという背景があります。
[^2]: 参考にしている論文では "multimodal deep learning framework" と呼んでおり、最近の大規模基盤モデルで期待されるマルチモーダルについても何らかの示唆がある気がしていますが、まだまだ勉強不足です...。
[^3]: 最近では pseudo label は広義の疑似ラベル作成（基盤モデルによる作成、教師モデルによる作成 etc）という意味合いで用いられますが、元々は学習中のモデル自身が作成するという意味合いでした。
[^4]: 一口に半教師あり学習と言っても大量に手法がある（サーベイ論文では52個の手法）のだと驚きました。