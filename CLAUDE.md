# uml-work01

UML・設計図を draw.io で描く練習用のリポジトリ。

## 構成
- `docs/diagrams/` … 図の置き場所。形式ごとに、次の 2 つのフォルダに分ける
  - `docs/diagrams/drawio/` … 図の元データ（`.drawio`）。作成・修正はこちらに対して行う
  - `docs/diagrams/svg/` … 表示用の画像（`.svg`）。人が VS Code の Export で作る
- `docs/design.md` … 図を埋め込んだ設計資料
- `docs/notes.md` … AI が作った図のレビュー記録。ハーネス改善の材料

## 作業のルール
- draw.io の図を作成・修正するときは、必ず `drawio-diagram` スキルに従う
- 既存の図は、指示がない限り上書きしない
- `.drawio` を保存すると、hook がチェックスクリプトを自動で実行する。エラーが返ってきたら、すべて直してから作業を終える
