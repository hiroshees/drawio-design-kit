# ER図

- IE 記法（鳥の足記法）で描く
- テーブルは、swimlane＋行の図形で描く。見出しは「論理名 / 物理名」（例：`社員 / employees`）
- 主キーの列を先頭に置き、主キーとそれ以外の列の間に区切り線（`line` の行）を入れる
- 列の行は「列名 : 型」とし、PK・FK の印は後ろに付ける（列名の頭をそろえるため）
  - 例：`id : BIGINT (PK)`、`employee_id : BIGINT (FK → employees.id)`、`name : VARCHAR(50)`
- 外部キー制約を付ける前提。FK の列には、必ず参照先（テーブル.列）を書く
- リレーションの線は、source を親テーブル（参照される側）、target を子テーブル（FK を持つ側）にする
  - 親側は `startArrow=ERmandOne`、子側は多重度に合わせて `endArrow=ERzeroToMany`（0以上）／`ERoneToMany`（1以上）／`ERzeroToOne`（0か1）
- リレーション名は、**すべての線**にラベルとして付ける
