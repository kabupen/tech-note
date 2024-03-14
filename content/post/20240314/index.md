+++
title = 'エッジデバイス界隈のR&D動向調査①'
date = 2024-03-14T00:00:16+09:00
draft = false
math = true
categories = ["技術調査"]
tags = []
toc = true
+++


各企業のホームページに上げられている事項をまとめ、各社現在どのような R&D を行っているのかを垣間見たいと思います。


## OKI

### 駐車場検知

OKI との協業で、エッジデバイスでの駐車場空車検知を行っています。車両検知や画層認識などの個々の技術としては確立されているものの、それらを融合して用いる場合に様々な課題が生じるという、社会応用のお手本のような取り組みかと思いました。

- https://www.oki.com/jp/case/2023/kurume-it.html?utm_source=aiedge


### フライングビュー

複数カメラの画像を合成することで俯瞰画像を作成する技術。機材の周辺360°を自由な視点でリアルタイムで俯瞰することができるもの。航行する船舶などでゆうこうになったりする。合成処理はFPGA上で実装してて、小型・省電力での映像処理を実現しているものです。

- [プレスリリース:海上・港湾・航空技術研究所とOKI、自動運航船の安全および船員負荷低減を目指した遠隔監視・遠隔操船に関する共同研究契約を締結](https://www.oki.com/jp/press/2021/06/z21019.html)

### 配送計画最適化サービス

物流では様々な問題を抱えており効率化が必須で、そのために配送計画の最適化サービスを SaaS として提供しているとのことです。

- https://www.oki.com/jp/press/2023/03/z22083.html


### 水中音響通信技術

自立型無人潜水機などで使用される水中 IoT 機器同士（水中ドローンなども）の通信において、高速通信の実証実験に成功しています。ドップラー効果、反射などの課題を解決した水中の通信技術を確立していて、沖合養殖の設備管理や海洋資源調査など、海洋産業の効率化や新たなビジネスの創出が可能となるようです[^2]。

- https://www.oki.com/jp/press/2023/06/z23024.html


### AI画像処理速度の高速化

OKI が開発したAIモデルの軽量化技術 PCAS (Pruning Channels with Attention Statistics) [^1] を利用して、顧客の持つAIプログラムの軽量化を自動で行うことができる技術です。また FPGA 実装までを自動化することで効率化を図ることができる模様です。FPGA回路設計自動化部分は Zebra と呼ばれる技術と融合しているようです。


### 適切な量子化値を割り当てる手法の開発


新エネルギー・産業技術総合開発機構（NEDO）との協業で、「高効率・高速処理を可能とするAIチップ・次世代コンピューティングの技術開発」において AI の学習時に量子化値を最適に割り当てる低ビット量子化技術「LCQ（Learnable Companding Quantization）」を開発したそうです。エッジ領域での高精細な画像認識、さらには工場のインフラ管理や機器の異常検知など、演算リソースの限られたデバイスでのAI実装に応用が期待されます。

- https://www.oki.com/jp/press/2021/06/z21026.html
- [Learnable Companding Quantization for Accurate Low-bit Neural Networks](https://openaccess.thecvf.com/content/CVPR2021/papers/Yamamoto_Learnable_Companding_Quantization_for_Accurate_Low-Bit_Neural_Networks_CVPR_2021_paper.pdf)



### CounterSmart

接客支援ミドルウェア「CounterSmart」に搭載した感情AI技術の1つである「興味・関心推定技術」を用い、端末のカメラから得た表情データと視線センサーから得た視線データから、興味・関心が高そうなメニューを提案する PoC を実施していたようです。接客対応時間の短縮などの効率化も見込むようです。

- https://www.oki.com/jp/enterprisedx/storefront/countersmart/




## NTTドコモ

- https://www.docomo.ne.jp/corporate/technology/rd/technical_journal/index.html

### CAI/C2PA

アドベントカレンダーですが、生成AI コンテンツの来歴照明技術について述べられています。これから生成AIで作成したコンテンツについて、どのように本物か生成画像化を見分けるための技術として必須となってきそうです。


- https://nttdocomo-developers.jp/entry/20231224_2



### 3D Gaussian Splatting


サービスイノベーション部では三次元再構成技術に関する研究開発を行っているようで、2020年に登場した NeRF に始まり、2023年に提案された 3D Gaussian Splatting について述べられています。




### スマートフォンログを用いた血圧上昇習慣推定AIの開発

スマートフォンログ（運動情報、位置情報など）、属性データ（年齢、性別）などを用いて、血圧上昇の習慣があるかどうかのフィードバックを返すための AI を作成した。いわゆる「行動変容」に関する研究開発だと思われる。


- https://www.docomo.ne.jp/corporate/technology/rd/technical_journal/bn/vol31_4/003.html




## KDDI


以下の図が、研究開発（R&D）と社会応用に関して分かりやすかったので[引用](https://www.kddi.com/corporate/r-and-d/system/)します。研究開発も重要なのですが、やはりそれを社会（市場）に還元するための技術実証が必要なのだと痛感します。

{{< figure src="./20240315-011335.png" width=400 >}}


### 情報処理学会「優秀論文賞」：スマートフォン位置情報を用いた個人における自然災害の曝露量推定


## 三栄ハイテックス


### エッジデバイス実装


顧客が持っているアルゴリズムから、HWに適したアーキテクチャを提案し、最適なソリューションを実現しているとのこと。FPGA（Zynq UltraScale+）でのセマンティックセグメンテーションの高速実行などのデモが面白い。40 FPS の高速化を達成しているとのことです。PixelNet をターゲットとしてまずモデル自体の軽量化を行い、その上で FPGA へ実装するための最適化を行うことで、高速リアルタイム推論を実現したとのことです。

- https://www.sanei-hy.co.jp/business/ai/edge-device/
- https://www.sanei-hy.co.jp/business/ai/algorithm/#case01



## その他キーワード


- ローカル5G
- モデル軽量化
- 人工意識による高度自律的学習機能の研究開発
- ドローン制御技術
- エッジ・クラウド連携技術
- 「革新的AIエッジコンピューティング技術の開発　発表資料」


[^1]: その他には、CP、ThiNet、SSS などの手法が一般的だそうです。
[^2]: 新しい技術をみると（それがどのような応用先か分からないほど）ワクワクしますね。
