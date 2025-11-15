+++
title = 'VSCodeのオレオレ設定'
date = 2024-12-24T11:25:49+09:00
draft = false
categories = []
tags = []
+++


## Vim

- コード置き場（[github](https://github.com/kabupen/setup/tree/main/vscode)）

### 

```json
// ハイライト表示
"vim.hlsearch" : true, 
// 入力中にも検索
"vim.incsearch": true,
// ヤンクとコピペのレジストリを同期する
"vim.useSystemClipboard": true, 
// leader を <space> キーにマッピング
"vim.leader": "<space>",
```

### ノーマルモード

```json
"vim.normalModeKeyBindings": [
    // vim の undo を VSCode のundoにする
    { "before" : ["u"], "commands" : ["undo"] }, 
    // vim の redo を VSCode の redo に割り当てる
    { "before" : ["<C-r>"], "commands" : ["redo"] }, 
    // ハイライトを消す
    { "before": ["C-n"], "commands": [ ":nohl" ] }, 
    //　変数の参照箇所を表示
    { "before": [ "g", "f" ], "commands": [ "editor.action.referenceSearch.trigger" ] }, 
    // エクスプローラーへ移動
    { "before": [ "<leader>", "e" ], "commands": [ "workbench.view.explorer" ] }, 
],
```

### インサートモード

```json
"vim.insertModeKeyBindings": [
    // サジェストの発火
    { "before" : ["<C-m>"], "commandas" : ["editor.action.triggerSuggest"] } 
],
```