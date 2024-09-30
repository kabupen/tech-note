

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