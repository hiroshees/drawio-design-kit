# シーケンス図

## ライフライン
- `shape=umlLifeline` を使う
- アクターは `participant=umlActor` とする。名前が棒人間と重ならないよう `verticalAlign=top` を付け、`spacingTop` は `size` より大きくする（例：`size=40;spacingTop=42`）
- 活性区間（Activation）を置く

## メッセージ
- 呼び出し：実線＋塗りつぶしの三角（`endArrow=block;endFill=1`）
- 戻り値：点線＋開いた矢印（`dashed=1;endArrow=open;endFill=0`）
- 送る側から受け取る側へ引く
- メッセージは活性区間に連結しない。source／target は指定せず、`sourcePoint`／`targetPoint` で座標を指定し、両端を活性区間の左右の端にそろえる
- メッセージは上から順に、30〜40px 間隔で y をずらす（同じ y のメッセージを作らない）。戻り値は、対応する呼び出しより下に置く

## 複合フラグメント（alt など）
- 枠（`shape=umlFrame`）は XML の最後に置く（最前面にする）
- 見出しは白、枠の中は透明（`fillColor=#FFFFFF;swimlaneFillColor=none`）
- ガード条件は枠内のテキストで書く。区画の区切りは点線
