+++
title = 'Swift でカメラアプリを作成する'
date = 2024-04-27T09:36:13+09:00
draft = false
math = true
categories = ["Swift"]
tags = []
toc = true
+++


[SwiftUI](https://developer.apple.com/documentation/swiftui) について概要をまとめます。SwiftUI については [Introducing SwiftUI](https://developer.apple.com/tutorials/SwiftUI) のチュートリアルが非常に丁寧だと思いますので、そちらに目を通しつつ理解を深めていきたいと思います。


## SwiftUI

SwiftUI とは 2019年に導入された UI フレームワークの一つで、コードベースで UI を作成することができるものです。以下のようなコードで、Hello World の画面を簡単に作成することができます。

{{< figure src=./20240427-095044.png width=500 >}}


### UIViewRepresentable

UIKit の機能を SwiftUI でも使用できるようにしているラッパーで、`makeUIView` と `updateUIView` の2つの実装が必要となります。

## UIKit

UIKit も UI フレームワークの一つで、Storyboard/XIB ファイルを利用して UI を作成することができるものです。ただし2007年から開発・利用されているものですので、様々な情報が豊富であることや使用できる機能も豊富であることから、現在でも UIKit を使用した開発も行われています[^1]。


### UIView



スクリーン上の矩形領域のコンテンツを管理するためのクラスです。



### UIViewController


## 必要なファイル


## アーキテクチャ

iOS アプリのアーキテクチャバターンでは MVC (Model-View-Controller)、MVVM (Model-View-View Model)、MVP がよく知られているもので

MVC では処理を

- Model
- View
- Controller

の３つの構造に分割して実装しいきます。


ViewModel には一般的にはデータの処理に関するコードを書いていき、View (`UIView`、`UIViewController`) には表示するためのコードを書きます。


https://dev.classmethod.jp/articles/practice_ios-architecture-pattern/

SwiftUI では MVVM を採用しています。


## CameraViewModel


### カメラの権限要求

iOS ではカメラを使用するときにはカメラアクセスをユーザーに許諾してもらう必要があります。権限要求のためのアラート画面（ポップアップ）は `AVCaptureDevice.requestAccess` で表示することができます。`authorizationStatus` と組み合わせることで

```java
switch AVCaptureDevice.authorizationStatus(for: .video) {
case .authorized:
    isCameraAuthorized = true
case .notDetermined:
    AVCaptureDevice.requestAccess(for: .video) { authorized in
        DispatchQueue.main.async {
            self.isCameraAuthorized = authorized
            if authorized {
                self.setupSession()
            }
        }
    }
default:
    isCameraAuthorized = false
}
```

まだ許可されていない場合にアラートを表示するような実装にしておきます。


で

## CameraView
## ContentView




[^1]: SwiftUI か UIKit のどちらを使用するかという問題 (?) は世の中にたくさんのブログが出回っています。