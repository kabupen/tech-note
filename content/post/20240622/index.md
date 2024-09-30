+++
title = '不偏分散'
date = 2024-06-22
draft = false
math = true
categories = ["統計検定"]
tags = []
toc = false
+++



## レンダリング

3次元情報を2次元情報に変換して、「画像」として出力することをレンダリングと呼びます。3DCGのレンダリング手法は大きく分けて

- ラスタライズ法
- レイトレーシング法

に分けられます。レイトレーシング法の方が現実世界の視界への光の入力を高度にエミュレートできるため高品質なグラフィックスを実現できるのですが、高負荷処理であるためリアルタイム性にかけるという欠点があります。そのためゲームエンジンなどではラスタライズ法が用いられるのが一般的です。


## ラスタライズ



- シェーディング
- グラフィックスパイプライン



ピクセルが対応する三角形IDを求める
barycentric 補完
シルエット勾配
tf_mesh_render
OpenDR

- レンダリングプリミティブ（基本図形）
- フラグメントデータ
- ラスタ化処理（ラスタライズ）
  - ヒルベルト曲線
- スキャンコンバージョン（走査変換）
  - 図形によって覆われる画素を選択する
  - 

## 参考文献

- https://www.mlit.go.jp/plateau/file/libraries/doc/plateau_tech_doc_0060_ver01.pdf
- https://www.ipsj-kyushu.jp/page/ronbun/hinokuni/1003/5A/5A-3.pdf
- https://speakerdeck.com/hsato/wei-fen-ke-neng-rendaranotukurikata-li-lun-karavulkanshi-zhuang-made?slide=69
- https://tokoik.github.io/gg/ggnote01.pdf
- https://tokoik.github.io/gg/ggnote01.pdf