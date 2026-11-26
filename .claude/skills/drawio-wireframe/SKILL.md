---
name: drawio-wireframe
description: outputs/wireframes/ の画面ワイヤーフレーム（.drawio）を新規作成・修正するときに使う。PC（1280×800）とスマホ（375×812）の画面を、draw.io の Mockups 図形で描く。UML 図・ER 図・画面遷移図には使わない（それらは drawio-diagram スキル）。
---

# draw.io ワイヤーフレーム作図スキル

## 手順

1. `references/rules.md` と `references/catalog.md` を読む。読まずに描き始めない
2. 画面の要素（部品）を一覧にして、確認を取る
   - 内容に書かれていないことは、推測で埋めず、「不明点」として一覧の最後に挙げる
   - 画面遷移図など、ほかの図との連動は不要。連想の元にするのはかまわない
   - 修正のときは、変更する箇所だけを示せばよい
3. ファイル名を `wf-<画面ID>-<名前>.drawio` にする（例：`wf-sc01-login.drawio`）。ページは、PC 版を `pc`、スマホ版を `sp` にする
   - メニューを開いた状態などを描くときは、`sp-menu` のように「-状態名」を付けたページを足す（`references/rules.md` の 1）
   - 同じ名前のファイルがすでにあれば、上書きせずに別の名前にする
4. `.drawio` を書く
   - 見本は `outputs/wireframes/drawio/wf-sc01-login.drawio`。構造（レイヤー、画面枠、注釈）をそろえる
   - 図形は `references/catalog.md` の「採用」から選ぶ。図形の中の文字は、`value` ではなく属性（`mainText` など）で指定する
   - 作成中は、`.drawio` を VS Code の draw.io エディタで開かない（意図しない保存で壊れることがある）
5. 保存すると、hook がチェックスクリプトを実行する。エラーが返ってきたら、すべて直す
6. `scripts/export_wireframe.sh outputs/wireframes/drawio/<ファイル名>.drawio` を実行する。ページごとに、SVG と PNG が書き出される
7. PNG を読み込んで、見た目を確認する（下の「作成後のセルフチェック」）。直したら、5 から繰り返す
8. 報告する。セルフチェックの結果と、`export_wireframe.sh` の実行結果（OK / NG と、出力したファイル）を含める

## ファイル

- 元データは `outputs/wireframes/drawio/` の `.drawio`（非圧縮の XML）。作成・修正はこのファイルに対して行う
- 表示用の `.svg` と、確認用の `.png` は、`scripts/export_wireframe.sh` で `outputs/wireframes/svg/`、`outputs/wireframes/png/` に書き出す。直接作成・編集しない
  - `.png` は git に入れない（`.gitignore` 済み）
- `<mxGraphModel>` に `background="#FFFFFF"` と `gridSize="8"` を指定する
- UML 図とは、書き出しのスクリプトも、チェックの内容も別。UML の `scripts/export_svg.sh` は使わない

## 作成後のセルフチェック

hook が機械的に確かめられない点を、PNG を見て確認する。

1. 図形やラベルが重なっていないか。図形の中に、既定の英文字（Main Text、Option 1 など）が残っていないか
2. 注釈の番号丸が、対応する部品の左上にあるか。補足文の番号と、丸の番号が合っているか
3. 余白と間隔が、`references/rules.md` のとおりか（画面端の余白、ラベルと入力欄の間隔など）
4. 文字の大きさ、色が、ルールのとおりか。赤を、注釈以外に使っていないか
5. `pc` と `sp` の内容が、画面として対応しているか

## 追加の図形が必要なとき

`references/catalog.md` にない図形は、使わない。「図形を追加するとき」の手順で、描画を確認してから、採用リストに追加する。
