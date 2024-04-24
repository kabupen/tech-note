+++
title = 'AVFoundation について'
date = 2024-04-24T22:21:35+09:00
draft = true
math = true
categories = ["Swift"]
tags = []
toc = true
+++


[AVFoundation](https://developer.apple.com/av-foundation/) は iOS/macOS/watchOS/tvOS で動作するフレームワークで、動画などのメディアを扱うための基盤となっています。本稿ではその AVFoundation についての概要を説明してみたいと思います。


## Capture

[AVFoundation Capture subsystem](https://developer.apple.com/documentation/avfoundation/capture_setup)とは動画、画像、音声を扱うための仕組みです。Capture の主な構成は sessions, inputs, outputs です。入出力を Capture  session が繋いでいるというイメージで、このセッションを開始することでデータが流れるというイメージです。初期化用の関数の中で、デバイスの設定、入力の設定、出力の設定をセッションに紐づけていきます。

{{< figure src=./20240424-223844.png width=600 >}}

























## Capture Session の一例

[AVCaptureSession](https://developer.apple.com/documentation/avfoundation/capture_setup/setting_up_a_capture_session) がベースのクラスで、カメラデバイスとの接続から出力までを行うことができます。以下に capture session の一例を挙げます。カメラ入力から同画像処理を行うためのセッションを定義しています。

{{< figure src=./20240424-224135.png width=600 >}}


### Display a Camera Preview

画像の撮影前、動画の録画開始前にユーザーにプレビュー（今どのような画像がカメラ内で撮影されているか）を表示しておくのが UX の観点からも重要です。そのためのクラスが [AVCaptureVideoPreviewLayer](https://developer.apple.com/documentation/avfoundation/avcapturevideopreviewlayer) であり、セッションが生きている間は自動で live video を画面に出力することができます。

UIView は [CALayer](https://developer.apple.com/documentation/quartzcore/calayer) を背後に持っていて、このレイヤー上に各種描画処理が行われていきます。AVCaptureVideoPreviewLayer を CALayer に追加することで、カメラの映像が UI 上に表示されるようになります。


### Run the Capture Session 

AVFoundation に関する入出力、プレビューの設定が終わったあとで、`startRunning()` を実行することでセッションが開始し、実際の入出力が行われます。


## Capture devices

どのデバイスのどんなモード（ex. back/front camera）を使用するかなどを管理する必要があります。デバイスは [AVCaptureDevice](https://developer.apple.com/documentation/avfoundation/avcapturedevice) で管理されています。デバイスからの入力情報は [AVCaptureDeviceInput](https://developer.apple.com/documentation/avfoundation/capture_setup/choosing_a_capture_device) で管理されています。



