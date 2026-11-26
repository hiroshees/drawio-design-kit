# uml-work01

UML・設計図を draw.io で描く練習用のリポジトリ。

## 構成
- `outputs/` … 成果物の置き場所
  - `outputs/uml/` … UML 図・ER 図。形式ごとに、次の 2 つのフォルダに分ける
    - `outputs/uml/drawio/` … 図の元データ（`.drawio`）。作成・修正はこちらに対して行う
    - `outputs/uml/svg/` … 表示用の画像（`.svg`）。`scripts/export_svg.sh` で書き出す（直接作成・編集しない）
  - `outputs/wireframes/` … 画面のワイヤーフレーム。`drawio/`（元データ。1 ファイルに `pc`・`sp` のページ。別の状態は `sp-menu` などのページを足す）、`svg/`（表示用）、`png/`（Claude Code の確認用。git に入れない）、`catalog/`（部品カタログの元データと、確認用の画像。画像は git に入れない）
- `review/` … 成果物を確認するための MD
  - `review/uml.md` … UML 図・ER 図を埋め込んだ資料
  - `review/wireframes.md` … ワイヤーフレームを埋め込んだ資料
- `agent-notes/notes.md` … AI が作った図のレビュー記録。ハーネス改善の材料

## 作業のルール
- draw.io の図は、置き場所（作る図の種類）で従うスキルを使い分ける
  - UML 図・ER 図（`outputs/uml/`）：必ず `drawio-diagram` スキルに従う。書き出しは `scripts/export_svg.sh`
  - ワイヤーフレーム（`outputs/wireframes/`）：必ず `drawio-wireframe` スキルに従う。`drawio-diagram` スキルは使わない。書き出しは `scripts/export_wireframe.sh`（ページごとに SVG と PNG）
- 既存の図は、指示がない限り上書きしない
- `.drawio` を保存すると、hook がチェックスクリプトを自動で実行する。チェックの内容は、フォルダ（`outputs/uml/` か `outputs/wireframes/`）で切り替わる。エラーが返ってきたら、すべて直してから作業を終える
- `.drawio` は、作成中に VS Code の draw.io エディタで開かない（意図しない保存で壊れることがある）
