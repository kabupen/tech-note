
# ディレクトリ構造


```
sample/
├── archetypes/
│   └── default.md
├── assets/
├── content/
├── data/
├── layouts/
├── public/
├── static/
├── themes/
└── config.toml
```


- archetypes: markdown のテンプレートを保存する
- assets
- content
  - webサイトのすべての記事を置く
- data
  - サイトの全ページから参照したいデータを格納
- layouts
  - themes ディレクトリのテーマを修正する、追加機能を実装するときに使用
- static
  - 画像、CSS、JavaScript などの静的ファイルを格納
  - 記事に画像を貼る場合もここに格納する

## 設定ファイル

- v0.109.0 までは config.toml を使用していたが、新しいバージョンでは hugo.toml を利用のこと


## layouts

- 自作の html ヘッダーを読み込むことができる


### hugo-bearblog

- layouts/partials/custom_head.html を配置
  - ここに追加したい html を記述すると全ページのヘッダーに読み込まれる
  - ex. Katex の設定


# 各パーツ

## menu

- layouts/partials/nav.html で定義
  - content 以下に <directory>/index.md の構造であれば自動でメニューに表示されるかも
  - hugo.toml で main 以外を定義している