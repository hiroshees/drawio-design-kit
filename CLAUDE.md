# uml-work01

UML・設計図を draw.io で描く練習用のリポジトリ。

## 構成
- `outputs/` … 成果物の置き場所
  - `outputs/uml/` … UML 図・ER 図。形式ごとに、次の 2 つのフォルダに分ける
    - `outputs/uml/drawio/` … 図の元データ（`.drawio`）。作成・修正はこちらに対して行う
    - `outputs/uml/svg/` … 表示用の画像（`.svg`）。`scripts/export_svg.sh` で書き出す（直接作成・編集しない）
  - `outputs/wireframes/` … ワイヤーフレーム（`drawio/`・`svg/`・`png/`）。準備中で、作成のルールは未整備
- `review/` … 成果物を確認するための MD
  - `review/uml.md` … UML 図・ER 図を埋め込んだ資料
- `agent-notes/notes.md` … AI が作った図のレビュー記録。ハーネス改善の材料

## 作業のルール
- draw.io の図を作成・修正するときは、必ず `drawio-diagram` スキルに従う
- 既存の図は、指示がない限り上書きしない
- `.drawio` を保存すると、hook がチェックスクリプトを自動で実行する。エラーが返ってきたら、すべて直してから作業を終える
