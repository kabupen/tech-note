+++
title = '波形データ解析のあれこれ'
date = 2024-03-03T10:18:29+09:00
draft = true
math = true
tags = []
categories = []
toc = true
+++


## フーリエ解析について

フーリエ級数とは周期関数を三角関数の級数（和の形）で表すものですが、それらをより一般的な非周期関数へ拡張したものがフーリエ変換です。このフーリエ級数展開、フーリエ変換を用いて波形データを解析していく手法が、フーリエ解析となります。


### 余談

まず初めに余談として、三角関数周りで使用する "文字" についてまとめておきます。

実世界で波形データを観測するときには、一般的には時間 [sec] の単位でデータを収集することと思います。しかし三角関数の単位は $\theta$ [rad] ですので、「取得した時刻 $t=T^\prime$ での値は...$\sin T^\prime$」の様には計算できません。そのため単位を変換する過程で色々と "文字" が出てきます。

{{< figure src="20240303-111432.png" width="500" >}} 


周期 $T$ [sec] で取得した正弦波データを定式化するためには、

$$
\theta = \frac{2\pi}{T} t
$$

という関係式を用います。また、$2\pi/T$ の部分は「1秒あたりの角度情報」として各周波数 $\omega$ を用いると、正弦波の定式化は

$$
y = \sin \frac{2\pi}{T} t =  \sin \omega t
$$

のように表現できます。周期 $T$、各周波数 $\omega$ ともに、三角関数の形状に関する量であることが分かります。






## フーリエ級数

周期 $T$ の関数 $f(t)$ は三角関数の無限級数（無限和）の形で表すことができ

$$
f(t) = \frac{a_0}{2}  + \sum_{n=1}^\infty \left\( a_n \cos \frac{2\pi nt}{T} + b_n \sin \frac{2\pi nt}{T} \right\)
$$

をフーリエ級数展開（または単にフーリエ級数）と呼びます。また、$a_n, b_n$ はフーリエ係数と呼ばれ


$$
a_n = \frac{2}{T} \int_{-T}^T f(t) \cos \frac{2\pi nt}{T} dt, ~~
b_n = \frac{2}{T} \int_{-T}^T f(t) \sin \frac{2\pi nt}{T} dt 
$$

で表されます。

フーリエ級数は複素関数を使って複素形式に書き直しておくことで式変形や計算の見通しが良くなるので、ここからは複素フーリエ級数を扱っていきます（複素フーリエ級数はオイラーの公式を用いることで導出することができます）。

$$
f(t) = \sum_{n=-\infty}^\infty c_n e^{i(2\pi n/T)t} \\\\
$$
$$
c_n = \frac{2}{T} \int_{-T/2}^{T/2} f(t) e^{-i(2\pi n/T)t} dt
$$



### 理論的背景

なぜ収束するか？




### 何が連続量か？


フーリエ級数の威力は、**離散的**な各周波数を持つ三角関数の級数として 周期関数 $f(t)$ が展開できるところにあります。例として $\cos$ の部分を見てみると

$$
\sum_{n=0}^\infty \cos \frac{2\pi n}{T} t = \cos \frac{2\pi}{T} t + \cos \left(\frac{2\pi}{T}\times 2 \right)t  + \cos \left(\frac{2\pi}{T}\times 3 \right)t + ... 
$$

のように、$2\pi/T$ を基本の単位としてその整数倍の周波数を持っています（$2\pi/T$ は基本周波数と呼ばれる量です）。そのため、周期関数をフーリエ級数展開すると下図のように $c_n$ は不連続な値を取ります。そのため $c_n$ は離散スペクトルと呼ばれます。











## フーリエ変換


フーリエ級数では周期関数を扱っていましたが、これを非周期関数（一般的な関数）へと拡張したものがフーリエ逆変換です。フーリエ逆変換は以下の式で定義されます[^2]：

$$
f(x) = \frac{1}{2\pi} \int_{-\infty}^\infty F(w) e^{i \omega x} dw
$$

フーリエ係数に相当する $F(\omega)$ はフーリエ変換として以下で定義されます[^1]

$$
F(\omega) = \int_{-\infty}^\infty f(x) e^{-i \omega x} dx
$$



### フーリエ級数の極限としてのフーリエ変換


数学的に厳密ではない（らしい）のですが、周期 $T$ の極限としてフーリエ変換を導出しておくことで直感的な理解の助けとなるので、以下で議論を追ってみます。










### フーリエ変換の定義式について

参考書、ブログなどでフーリエ変換の定義式がまちまちなことがあります。



### パワースペクトル （エネルギースペクトル）

フーリエ変換した関数の絶対値の二乗

$$
|F(\omega)|^2
$$

はパワースペクトル、またはエネルギースペクトルと呼ばれます。




## 離散フーリエ変換










## 補足：用語

### スペクトル（スペクトラム）

スペクトル（spectrum）とは波形信号を興味のある成分に分解して表したもので、光を波長ごとに分解する分光スペクトル、音声データを周波数ごとに分解する周波数スペクトルなどがあります。スペクトルは幅広い領域で使用されており、実験装置（分光器）でそもそもスペクトル分析を実施したり、または実験データにフーリエ変換適用することでスペクトルを解析したりなど、「波形信号を特定の量に分解する」というのを根本としています。


#### 分光スペクトル

例えば天文学において、観測された光を分光することで天体の組成や運動などを知ることができます。


{{< figure src="20240303-121743.png" width="400" >}} 



### スペクトログラム

スペクトログラム（Spectrogram）とは、ある時間毎に区切ってスペクトルを計算したもので、スペクトルのおおよその時間変化を解析することができるものです。






## librosa を用いた解析

さっそく本題に移っていきます。hx



### スペクトル解析











# 













## 離散フーリエ変換


波形データをフーリエ変換することで便利であることは分かったのですが、フーリエ変換を計算するためにはとある領域（ex. とある時間幅）での $f(x)$ を事前に知っておく必要があります。実験データとして無限に近しいデータ点を取得して関数の形を知る必要がるということですが、現実的ではありません。実際にはいくつかの実験データ点が取得できているのが一般的でしょう。

こういった場合では、離散フーリ変換（Discrite Fourier Transform; DFT）を用いることができます。

とある周期関数波形データを $f(x)$ として、今 $N$ 個のサンプル $f(t_0), f(t_1), ..., f(t_{N-1})$ を取得したとします。フーリエ変換では

$$
F(\omega) = \int_{-\infty}^\infty f(t) e^{-i\omega t} dt
$$








[^1]: 天下り的に導入しましたが、周期 $L$ に関するフーリエ級数展開の数式から、周期を無限大に拡張することで得られます。詳しくはその道の本を読んでみてください...。
[^2]: フーリエ級数展開のときには、「関数は三角関数の級数で表現できるのです！」という導入がされることが多いのですが、それを非周期連続関数に拡張すると、「フーリエ変換は...」という書き出しになり、その逆変換としてフーリエ逆変換が導入されます。いまいち言葉として対応していないのがいつも気になります。