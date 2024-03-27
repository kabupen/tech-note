+++
title = 'VAE理解までの道のり #3'
date = 2024-03-23T18:15:07+09:00
draft = false
math = true
categories = ["機械学習"]
tags = ["VAE"]
toc = true
+++


Variational Autoencoder（VAE）を理解するまでの道のりの第3回目のブログです。内容が重複する部分もありますが、復習も兼ねて議論していきたいと思います。

- [VAE理解までの道のり#1]()
- [VAE理解までの道のり#2]()



## VAE 

生成モデル（generative models）とは、対象ドメイン（画像、音声、etc）のデータを生成できるモデルのことです。データを用いて対象ドメインの分布 $p_\theta(x)$ を学習することで、そこからのサンプリングによって

$$
x \sim p_\theta(x)
$$

新しいデータを生成することができるようになります。生成モデルのうちここでは、隠れ変数 $z$ をもつモデル $p_\theta(x, z)$ について考えます。

モデルの学習（パラメータ $\theta$ の決定）には一般的には最尤法を用いることができます、潜在変数を持つモデルでは確率分布が計算不能（intractability）であることから一筋縄では学習することができないという問題があります。当該の生成モデルの周辺確立は

$$
p_\theta(x) = \int p_\theta(x, z) dz
$$

と計算することができ、実際の生成の際には $p_\theta(x)$ からのサンプリングが必要になります。しかし、

$$
p_\theta(x, z) = p_\theta(z|x)p_\theta(x)
$$

において posterior probability $p_\theta(z|x)$ が intractable であることから周辺確率 $p_\theta(x)$ も intractable な性質を持つことになります。そのため直接的に最尤法を用いて

$$
\log p_\theta(x)
$$

を計算して学習することは不可能であり、この問題をどのように解決するかによって各手法が提案されています。











## Evidence Lower Bound （ELBO）


### 前提

ここでの問題は、潜在変数 $z$ をもつモデルの学習を行いたいが $\log p_\theta(x)$ を直接計算することができないという点です。そのため一般的な変分推論の枠組みでは $\log p_\theta(x)$ の下限値（evidence lower bound; ELBO）を導出することで、ELBO の最適化問題に置き換えて考え行く手法が採られます。

潜在変数に関する**任意の確率分布** $q(z)$ を用いることで、対数尤度は次のように変形できます。

$$
\begin{aligned}
\log p_\theta(x) &= \int q(z) \log \frac{p_\theta(x, z)}{q(z)}dz + \int q(z) \log \frac{q(z)}{p_\theta(z|x)} dz \\\\
&= L(q(z), \theta) + D_{KL}(q(z)||p(z|x))
\end{aligned}
$$

第二項はカルバック・ライブラー情報量であり非負の値であることから

$$
\begin{aligned}
\log p_\theta(x) \geq &= L(q(z), \theta)
\end{aligned}
$$

の関係式が導出でき、このことから $L(q(z), \theta)$ が evidence lower bound と呼ばれます。


### EMアルゴリズムにおける ELBO について


EM アルゴリズムは潜在変数を持つモデルの学習手法のひとつで、上述の

$$
\log p_\theta(x) = L(q(z), \theta) + D_{KL}(q(z)||p(z|x))
$$

の関係式を使って逐次的に最適化を行う手法です。以下に簡単に概要をまとめておきます。


#### E ステップ

まず、パラメータ $\theta$ をある値 $\theta^{\rm{old}}$ に初期化し、$q(z)$ に関して $L(q, \theta^{\rm{old}})$ を最大化します。$\log p_\theta(x)$ は $q(z)$ に依存しないため定数となり、

$$
\log p_{\theta^{\rm{old}}}(x) = Cost. = L(q(z), \theta^{\rm{old}}) + D_{KL}(q(z)||p_{\theta^{\rm{old}}}(z|x))
$$

の関係から、$L$ が最大となるためには $D_{KL}(q(z)||p(z|x)) = 0$ となればいいことが分かります。カルバック・ライブラー情報量の性質から

$$
q(z) = p_{\theta^{\rm{old}}}(z|x)
$$

の場合であることが分かり、Eステップを終えます。


{{< figure src=./20240327-135329.png  width=400 >}}



#### M ステップ

続いて M ステップでは

$$
q(z) = p_{\theta^{\rm{old}}}(z|x)
$$

と固定した状態で $L(q(z), \theta)$ を $\theta$ に関して最大化し、$\theta^{\rm{new}}$ を求めます。このとき

$$
D_{KL}(q(z)||p_{\theta^{\rm{new}}}(z|x)) \neq 0
$$

となるので、再度 E ステップを実行することになります。



{{< figure src="./20240327-135412.png" width=350 >}}



### VAE における ELBO について

EM アルゴリズムでは逐次的に ELBO の最適化問題を解くことで、$\theta$ を求めていきました。その一方でVAE では、学習可能なパラメーター $\phi$ を持った近似分布

$$
q_\phi(z|x) \simeq p_\theta(z|x)
$$

を導入し、これを用いて ELBO の最適化を行います。

それではまず、ELBO を導出してみます。以下の導出は $q_\phi(z|x) \to q(z)$ と置き換えることで、一般的な ELBO の導出過程と等しくなることに留意して下さい。

$$
\begin{aligned}
\log p_\theta(x)
&= \int q_\phi(z|x) \log p_\theta(x) dz \\\\
&= \int q_\phi(z|x) \log \frac{p_\theta(x, z)}{p_\theta(z|x)} dz \\\\
&= \int q_\phi(z|x) \log \frac{p_\theta(x, z)}{q_\phi(z|x)}\frac{q_\phi(z|x)}{p_\theta(z|x)} dz \\\\
&= \int q_\phi(z|x) \log \frac{p_\theta(x, z)}{q_\phi(z|x)}dz + \int q_\phi(z|x) \log \frac{q_\phi(z|x)}{p_\theta(z|x)} dz \\\\
\end{aligned}
$$

一行目は $\int q_\phi(z|x)~dz = 1$ を、二行目はベイズの定理を用いています。

第二項目は

$$
D_{KL}(q_\phi(z|x)|| p_\theta(z|x)) = \int q_\phi(z|x) \log \frac{q_\phi(z|x)}{p_\theta(z|x)}  \geq 0
$$

カルバック・ライブラー情報量と呼ばれる "距離" に関するものです。真の事後確率分布 $p_\theta(z|x)$ と、近似分q布 $q_\phi(z|x)$ との近さの度合いを表しています。非負の値であることから対数尤度は、

$$
\log p_\theta(x) \geq \int q_\phi(z|x) \log \frac{p_\theta(x, z)}{q_\phi(z|x)}dz \equiv L_{\theta,\phi}(x)
$$

第一項を下限値に取ることが分かります。この項こそ Evidence Lower Bound（ELBO）と呼ばれる量で、一般的に変分推論で解析不能な対数尤度の代わりに用いられるものです（上記の導出はその他にイェンセンの不等式を用いる方法もあります）。

また以下の様な式変形をしておきます。

$$
L_{\theta,\phi}(x) = \log p_\theta(x) - D_{KL}(q_\phi(z|x)|| p_\theta(z|x)) 
$$

これらの関係式を眺めつつ、ELBO を最適化（最大化）することで次のことが言えます。

1. ELBO は $\log p_\theta(x)$ の下限値であることから、ELBO を最大化すると（間接的に）対数尤度の最大化に繋がり、モデルパラメータが決まります
2. ELBO を最大化すると $\log p_\theta(x) - D_{KL}(q_\phi(z|x)|| p_\theta(z|x))$ においてカルバック・ライブラー情報量が小さくなることが分かり、$q_\phi(z|x) \simeq p_\theta(z|x)$ のように近似精度が上がっていきます

ここまでは通常の変分推論に関する概要で、ELBO $L_{\theta,\phi}(x)$ をどのように最大化するかによって各手法へと分岐していきます。



### 用語について


符号理論（coding theory）の観点から、観測されない変数である潜在変数 $z$ は latent representation もしくは code と呼ばれます。そのため、VAE の論文では

$$
q_\phi(z|x)
$$

を、データ $x$ を code である $z$ へと変換するという意味合いで確率的なエンコーダ（encoder）と定義しています。また、潜在変数 $z$ からデータ $x$ を予測するという意味で

$$
p_\theta(x|z)
$$

を確率的なデコーダー（decoder）と呼んでいます。



## VAE


目標は事後分布である

$$
p_\theta(z|x)
$$

を推定することなのですが、これまで見てきたように通常解析的には求まらないため近似計算手法を導入するというストーリになります。VAE では

1. 変分下界（Evidence Lower Bound; ELBO）
3. 償却推論（Amortized inference）
4. 再パラメータ化トリック（Reparametrization trick）

の３つのアイデアを元に、**近似事後分布の計算**を行います。




### 償却変分推論 （amortized variational inference）



事後分布を求めるための近似手法の一つとして、変分推論（variational inference）という手法があります。これはパラメータ化された分布

$$
q_\phi(z|x) \simeq p_\theta(z|x)
$$

を近似事後分布として導入し、パラメータ $\phi$ を最適化することで分布の形を求めるというものです。分布そのものを "変数" として求めるため、変分という名称が使用されています。


近似事後分布の求め方の一つに平均場近似と呼ばれる手法があります。この手法では近似分布がいくつかの分布の積で表すことができるという仮定のもとで

$$
p_\theta(z|x) \simeq q(z|\phi) = \prod_{i=1}^N q(z_i|\phi_i)
$$

とすることで近似計算を行っていきます。ここでは潜在変数 $z=\\{z_1,z_2,...,z_N\\}$ に対して変分パラメータ $\phi =\\{\phi_1, \phi_2,...,\phi_N\\}$ が対応しているとしています。ただし変分パラメータは事前にデータ点に対して最適な値を求めているため、直接データ $x$ に対する条件付き確率となっていないことに留意して下さい。また、$z$ に対して $\phi$ の個数は一致している必要はなく、例えば $q(\cdot)$ にガウス分布を使用する場合であれば潜在変数 $z$ 一つに対して、$\phi=\mu, \sigma$ の二つの変分パラメータが対応することになります。


上記の定義から分かるように、典型的な変分推論（ex. 平均場近似）ではデータ点 $x_i$ ごとに変分パラメータ $\phi_i$ の最適化が必要となるため、大規模なデータセットや新しいデータセットの推論が取り扱いにくいという問題がありました[^4]。


そこで償却変分推論ではデータ点ごとに変分パラメータを求めるのではなく、観測空間 $\Chi$ から確率密度関数空間 $P$ に写像するパラメトリックな関数 $f_\phi$ を導入することでこの問題に対処していきます[^3]。

まず、以下の平均場近似を考えます。

$$
q_\phi(z|x) = \prod_{i=1}^N q_\phi(z_i|x_i)
$$

このときに一般的には多変量ガウス分布を用いて

$$
q_\phi(z_i|x_i) = N(z_i| \mu(x_i), \sigma^2(x_i)I)
$$

のように定義します。ここで $\mu, \sigma$ はデータ点 $x_i$ をそれぞれガウス分布の平均値、分散に変換する非線形写像です。つまり償却変分推論とは、ニューラルネットワークなどのパラメトリックな関数を用いて変分パラメータを求め、それらを用いて事後分布を近似する手法です。




## 参考情報

- [Difference between AutoEncoder (AE) and Variational AutoEncoder (VAE)](https://towardsdatascience.com/difference-between-autoencoder-ae-and-variational-autoencoder-vae-ed7be1c038f2)
- [Disentangled な表現の教師なし学習手法の検証](https://tech.preferred.jp/ja/blog/disentangled-represetation/)


[^1]: [時系列データに対する Disentangle された表現学習](https://www.jstage.jst.go.jp/article/pjsai/JSAI2018/0/JSAI2018_1Z303/_pdf/-char/ja)
[^2]: [Disentangling by Factorising](https://arxiv.org/pdf/1802.05983.pdf)
[^3]: [集合を扱う償却変分推論](https://www.jstage.jst.go.jp/article/pjsai/JSAI2020/0/JSAI2020_2D4OS18a03/_pdf/-char/ja)
[^4]: [Advances in Variational Inference](https://ieeexplore.ieee.org/stamp/stamp.jsp?tp=&arnumber=8588399)