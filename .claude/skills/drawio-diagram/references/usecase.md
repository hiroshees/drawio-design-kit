# ユースケース図

- アクター：`shape=umlActor`。システムの枠の外に置く
- システムの枠：四角形。枠そのものにシステム名を入れ、文字は上寄せ
- 関連：矢印なしの実線（`endArrow=none`）
- include／extend：点線＋開いた矢印（`dashed=1;endArrow=open;endFill=0`）
  - include は基本 → 部品、extend は追加 → 基本の向き
  - extend の条件は、線のラベルの「«extend»」の下の行に「[条件]」と書く
- アクターの汎化：子 → 親に白抜きの三角（`endArrow=block;endFill=0`）。親と同じユースケースへの関連は、子には引かない
