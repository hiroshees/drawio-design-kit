# 部品カタログ（Mockups 図形）

`outputs/wireframes/catalog/catalog.drawio` の 1 ページ 1 カテゴリに、候補の図形を並べて描画を確認したもの。
PNG に書き出した画像で、描画できたことを確認した図形だけを「採用」にしている。図形名は draw.io 本体に実在するものだけを使った。

## 使い方の注意（確認で分かったこと）

- 図形の中の文字は、`value` ではなく**スタイルの属性**で指定するものが多い。`value` に書くと、図形の既定の英文字（Main Text など）と重なる
  - `mainText=`：ボタン、ボタンバー、ラジオ・チェックボックスのグループ、リンクバー、箇条書き、付箋、アコーディオン、パンくず、ステップバーなど。カンマ区切りで複数指定。先頭に `+` を付けた項目が選択中の表示になる
  - `linkText=`：リンク、吹き出し
  - `tabs=`：タブバー（`+` が選択中）
  - `subText=`：リストボックスの行（`mainText` は見出し）、アラートボックスの本文。`buttonText=` はアラートボックスのボタン
  - `value`（通常のラベル）で指定できるもの：テキスト入力、コンボボックス、検索ボックス、スピナー、ウィンドウのタイトル
- `mainText` が数字だけ（`mainText=1`）だと、書き出しが失敗する。全角の数字（`１`）なら書き出せる。「<」「>」は問題ない
- 日本語は問題なく描画できた
- `strokeColor` を指定しても、ラジオグループ、チェックボックスグループ、確認ダイアログ、検索欄、スピナーの枠は、ほかの部品より濃く（黒く）見える。原因は未確認で、許容している（`strokeColor=none` は効く）

## 採用（描画を確認できたもの）

| カテゴリ | 図形名 | 幅×高さ | 追加スタイル | 備考 |
| --- | --- | --- | --- | --- |
| buttons | `mxgraph.mockup.buttons.button` | 120×40 | `mainText=ボタン;strokeColor=#666666;fillColor=#dddddd;` |  |
| buttons | `mxgraph.mockup.buttons.horButtonBar` | 240×40 | `mainText=+ボタン1,ボタン2,ボタン3;` |  |
| buttons | `mxgraph.mockup.buttons.onOffButton` | 80×32 | `mainText=ON,OFF;` |  |
| forms | `mxgraph.mockup.text.textBox` | 200×32 | `mainText=;strokeColor=#666666;fillColor=#ffffff;align=left;spacingLeft=8;` |  |
| forms | `mxgraph.mockup.forms.pwField` | 200×32 | `mainText=******;` |  |
| forms | `mxgraph.mockup.forms.comboBox` | 200×32 | `strokeColor=#999999;fillColor=#ddeeff;align=left;fillColor2=#aaddff;mainText=;fontColor=#666666;spacingLeft=8;` | 文字の左の余白は `spacingLeft=8` で指定できる。`fontSize=14` も付ける |
| forms | `mxgraph.mockup.forms.checkbox` | 24×24 | `resizable=0;fillColor=#AAAAAA;gradientColor=#666666;strokeColor=#444444;` | 文字なし。**常にチェック済みの見た目**になる。未選択の見た目が要るときは、`checkboxGroup` を 1 項目（`+` なし）、`strokeColor=none` で使う |
| forms | `mxgraph.mockup.forms.radioGroup` | 160×64 | `mainText=+選択肢1,選択肢2;` |  |
| forms | `mxgraph.mockup.forms.checkboxGroup` | 160×64 | `mainText=+選択肢1,選択肢2;` |  |
| forms | `mxgraph.mockup.forms.searchBox` | 200×32 | `mainText=;flipH=1;align=left;spacingLeft=26;` |  |
| forms | `mxgraph.mockup.forms.signIn` | 240×176 | `mainText=ログイン,ユーザー名:,johndoe,パスワード:,********,パスワードを忘れた,新規ユーザー,ログイン,新規登録;` | 文言の並び順は mainText のカンマ区切り（見出し,ユーザー名ラベル,入力値,パスワードラベル,入力値,忘れた,新規ラベル,ログインボタン,登録ボタン） |
| forms | `mxgraph.mockup.forms.listBox` | 160×112 | `mainText=見出し;subText=項目1,+項目2,項目3;` |  |
| forms | `mxgraph.mockup.forms.spinner` | 120×32 | `spinLayout=right;spinStyle=normal;adjStyle=triangle;mainText=;align=left;spacingLeft=8;` |  |
| forms | `mxgraph.mockup.forms.horSlider` | 160×24 | `sliderStyle=basic;handleStyle=handle;` |  |
| forms | `mxgraph.mockup.forms.calendar` | 200×160 | `-` | 曜日と日付は英語固定（Su Mo Tu …）。文言を変える方法は未確認 |
| text | `mxgraph.mockup.text.link` | 120×24 | `linkText=リンク;` |  |
| text | `mxgraph.mockup.text.linkBar` | 240×24 | `mainText=ホーム,一覧,設定;` |  |
| text | `mxgraph.mockup.text.bulletedList` | 160×104 | `mainText=項目1,項目2,項目3;` |  |
| text | `mxgraph.mockup.text.stickyNote` | 160×80 | `mainText=メモ1,メモ2;` |  |
| text | `mxgraph.mockup.text.callout` | 160×64 | `linkText=吹き出し;callDir=NW;callStyle=line;strokeColor=#666666;fillColor=#ffffff;` | 枠なし。吹き出しの線が図形の外へ伸びる。注釈線として使う |
| containers | `mxgraph.mockup.containers.window` | 240×120 | `mainText=;align=center;verticalAlign=top;spacing=5;` |  |
| containers | `mxgraph.mockup.containers.browserWindow` | 320×160 | `mainText=https://example.com,ページ1;` |  |
| containers | `mxgraph.mockup.containers.alertBox` | 240×120 | `mainText=確認;subText=削除しますか?;buttonText=OK,キャンセル;` |  |
| containers | `mxgraph.mockup.containers.horTabBar` | 280×32 | `tabs=+タブ1,タブ2,タブ3;` |  |
| containers | `mxgraph.mockup.containers.verTabBar` | 120×120 | `tabs=+タブ1,タブ2,タブ3;` |  |
| containers | `mxgraph.mockup.containers.accordion` | 200×120 | `mainText=+グループ1,グループ2,グループ3;` |  |
| containers | `mxgraph.mockup.containers.marginRect` | 200×120 | `-` |  |
| navigation | `mxgraph.mockup.navigation.breadcrumb` | 240×24 | `mainText=ホーム,一覧,詳細;` |  |
| navigation | `mxgraph.mockup.navigation.pagination` | 96×24 | `linkText=;fontSize=14;fontColor=#008CFF;fontStyle=4;（value=「< 1 2 3 >」）` | 既定は小さい黒文字。`fontSize` などで、青い下線の文字にできる。箱は文字の幅（96）に合わせる |
| navigation | `mxgraph.mockup.navigation.stepBar` | 280×32 | `mainText=入力,確認,完了;` |  |
| navigation | `mxgraph.mockup.navigation.scrollBar` | 16×120 | `barPos=40;direction=north;resizeHeight=1;` |  |
| navigation | `mxgraph.mockup.navigation.pageControl` | 120×24 | `fillColor=#999999;strokeColor=#666666;` | 幅 120 以上で点が複数並ぶ（幅 64・高さ 16 では点が 1 つだけ） |
| misc | `mxgraph.mockup.misc.progressBar` | 200×16 | `fillColor2=#888888;barPos=60;` |  |
| misc | `mxgraph.mockup.misc.rating` | 120×24 | `-` |  |
| misc | `mxgraph.mockup.misc.shoppingCart` | 32×32 | `-` |  |
| misc | `mxgraph.mockup.misc.pin` | 24×32 | `-` |  |
| misc | `mxgraph.mockup.misc.map` | 200×120 | `-` | 既定の地図画像（変更不可） |
| misc | `mxgraph.mockup.misc.mail2` | 32×24 | `fillColor=#FFE040;` |  |
| misc | `mxgraph.mockup.misc.editIcon` | 32×32 | `-` |  |
| misc | `mxgraph.mockup.misc.trashcanIcon` | 32×32 | `-` |  |
| misc | `mxgraph.mockup.misc.help_icon` | 32×32 | `-` |  |
| graphics | `mxgraph.mockup.graphics.simpleIcon` | 32×32 | `strokeColor=#7E7E7E;fillColor=#111111;` |  |
| graphics | `mxgraph.mockup.graphics.barChart` | 160×120 | `strokeColor=none;strokeColor2=none;` |  |
| graphics | `mxgraph.mockup.graphics.columnChart` | 160×120 | `strokeColor=none;strokeColor2=none;` | 縦棒。2 系列（青と灰）、3 組で固定。本数や値は変えられない（未確認）。`barChart` は横棒 |
| graphics | `mxgraph.mockup.graphics.lineChart` | 160×120 | `strokeColor=none;` |  |
| graphics | `mxgraph.mockup.graphics.pieChart` | 120×120 | `parts=10,20,35;` |  |
| graphics | `mxgraph.mockup.graphics.iconGrid` | 120×120 | `-` |  |
| markup | `mxgraph.mockup.markup.redX` | 32×32 | `-` |  |

## 不採用（描画を確認したが、使えないもの）

| 図形名 | 理由 |
| --- | --- |
| `mxgraph.mockup.containers.group` | 高さの指定を無視して、ページの下まではみ出す（`container=1` を付けても同じ） |
| `mxgraph.mockup.markup.curlyBrace` | 指定した寸法どおりに描画されず、小さな波かっこになる。注釈には通常の線とテキストを使う |
| `mxgraph.mockup.misc.statusBar` | スマホのステータスバーではなく、青い部品が並んだ別の見た目になる |

## 未確認（候補に入れていないもの）

- `mxgraph.mockup.containers.*`（window など）の内側に部品を重ねたときの前後関係
- 文字サイズ・色の統一（フェーズ 2 のルールで決める）
- スマホ向けの図形（`mxgraph.mockup.mobile*`、iOS、Android）は今回の対象外

## 図形を追加するとき

1. 図形名は、推測で書かない。draw.io 本体に実在するか、描画して確かめる
2. `outputs/wireframes/catalog/catalog.drawio` に、新しい図形を置いて PNG に書き出し、画像で描画を確認する（`scripts/export_wireframe.sh outputs/wireframes/catalog/catalog.drawio` で、ページごとに書き出せる）
3. 描画できたものだけを、この文書の「採用」の表に追加する（チェックスクリプトは、この表を採用リストとして読む）。使えなかったものは「不採用」に、理由とともに書く
