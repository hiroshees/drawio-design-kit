---
name: drawio-diagram
description: outputs/uml/ の draw.io 図（.drawio）を新規作成・修正するときに使う。ユースケース図、クラス図、シーケンス図、アクティビティ図、ステートマシン図、ER図、画面遷移図に対応。ワイヤーフレーム（outputs/wireframes/）には使わない。
---

# draw.io 作図スキル

## 手順

1. 図の種類を決め、`references/` から該当するファイルを読む（下の表）。読まずに描き始めない
2. ファイル名を `<種類>-<名前>.drawio` にする（例：`er-study.drawio`）。種類の部分は下の表の「接頭辞」を使う。チェックスクリプトは、この接頭辞で図の種類を判断する
3. `.drawio` を書く
4. 保存すると hook がチェックスクリプトを実行する。エラーが返ってきたら直す
5. scripts/export_svg.sh を実行し、その結果を報告する

| 図               | 接頭辞      | 読むファイル           |
| ---------------- | ----------- | ---------------------- |
| ユースケース図   | `usecase-`  | references/usecase.md  |
| クラス図         | `class-`    | references/class.md    |
| シーケンス図     | `sequence-` | references/sequence.md |
| アクティビティ図 | `activity-` | references/activity.md |
| ステートマシン図 | `state-`    | references/state.md    |
| ER図             | `er-`       | references/er.md       |
| 画面遷移図       | `screen-`   | references/screen.md   |

## ファイル

- 図の元データは `outputs/uml/drawio` の `.drawio`（非圧縮の XML）。作成・修正はこのファイルに対して行う
- 表示用の `.svg` は、`scripts/export_svg.sh` で `outputs/uml/svg/` に書き出す。`.svg` を直接作成・編集しない
- `<mxfile>` に `scale="1"` と `border="20"` を指定する（画像の拡大率は等倍、余白は 20px）
- `<mxGraphModel>` に `background="#FFFFFF"` を指定する（背景は白で固定）

## 共通

- 線（edge）は必ず source と target を指定し、図形に連結する（端点を宙に浮かせない）。ただしシーケンス図のメッセージは例外（references/sequence.md を参照）
- 線のラベル（多重度、ガード条件、«include» など）は、独立したテキストではなく線のラベルとして付ける
- 図形どうし、ラベルどうしが重ならないように配置する。グリッドは 10px

## 作成後のセルフチェック

hook が機械的に確かめられない点を、自分で確認する。

1. 線のつなぎ先が、意味として正しいか（向き、どの図形につないだか）
2. 図形やラベルが重なっていないか
3. references のルールのうち、チェックスクリプトの対象外のもの（書式、配置など）を守っているか
