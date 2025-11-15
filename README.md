
# 執筆手順

1. 記事の新規作成
   1. content/post 以下に UUID 名のディレクトリ、index.md が作成される

```sh
python newpost.py
```



### ディレクトリ

https://gohugo.io/getting-started/directory-structure/

- archetypes
  - 記事のテンプレートを作ることができる
- assets
  - Hugo Pipes で処理するファイルを格納する
- content
  - 記事を置くディレクトリ
- data
  - サイトから参照するデータを置く
- layouts
  - thmemes を自分で編集するためのディレクトリ
- static
  - 画像、CSS などの全ての静的ファイルを格納するディレクトリ、記事に貼る画像もここに置く
  - ビルド時に public ディレクトリへコピーされる
- public
  - ビルド時に生成される
- resources
  - ビルド時に生成されるキャシュ

### hugo

```sh
$ hugo version        
hugo v0.122.0-b9a03bd59d5f71a529acb3e33f995e0ef332b3aa+extended darwin/arm64 BuildDate=2024-01-26T15:54:24Z VendorInfo=brew
```

### 設定ファイル

v0.109.0 以降は `hugo.toml` をルートディレクトリに配置する。


### Github Actions

- CI/CD の設定


# Hugo


## シンタックスハイライト

- hightlight.css の作成

```
hugo gen chromastyles --style=monokai > static/highlight.css
```



## ディレクトリ構造


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