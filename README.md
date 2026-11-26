# uml-work01

UML 図・ER 図・画面のワイヤーフレームを、draw.io で描く練習用のリポジトリです。
図は Claude Code に作らせます。スキル・チェックスクリプト・書き出しスクリプトで、作り方と品質をそろえています。

## できること

| 種類 | 内容 | 作り方 |
| --- | --- | --- |
| UML 図・ER 図 | ユースケース図、クラス図、シーケンス図、アクティビティ図、ステートマシン図、ER 図、画面遷移図 | `/create-diagram <種類> <内容>` |
| ワイヤーフレーム | 画面ごとに、PC 版（1280×800）とスマホ版（375×812）を描く。メニューを開いた状態などは、ページを足して描く | `/create-wireframe <画面ID> <名前> <内容>` |

作った図は、`review/` の Markdown で一覧できます。

- [review/uml.md](review/uml.md) … UML 図・ER 図
- [review/wireframes.md](review/wireframes.md) … ワイヤーフレーム

## フォルダ構成

```
.
├── outputs/                  成果物
│   ├── uml/
│   │   ├── drawio/           UML 図・ER 図の元データ（.drawio）
│   │   └── svg/              表示用の画像（書き出しで作る）
│   └── wireframes/
│       ├── drawio/           ワイヤーフレームの元データ（1 ファイル = 1 画面）
│       ├── svg/              表示用の画像（ページごと）
│       ├── png/              Claude Code が見た目を確かめる画像（git に入れない）
│       └── catalog/          部品カタログの元データ（catalog.drawio）と確認用の画像
├── review/                   成果物を確認するための Markdown
├── agent-notes/notes.md      AI が作った図のレビュー記録（ハーネス改善の材料）
├── scripts/
│   ├── export_svg.sh         UML 図・ER 図を SVG に書き出す
│   └── export_wireframe.sh   ワイヤーフレームを、ページごとに SVG と PNG に書き出す
├── .claude/
│   ├── settings.json         権限と hook の設定
│   ├── hooks/                .drawio を保存したときに動くチェックスクリプト
│   └── skills/               図の作り方（スキル）とコマンド
└── CLAUDE.md                 Claude Code への作業の指示
```

## 必要なもの

- [draw.io デスクトップ版](https://github.com/jgraph/drawio-desktop)（`drawio` コマンドで書き出す）
- Python 3（チェックスクリプト）
- Bash
- 画面のない環境では `xvfb-run`（WSLg がある WSL では不要）
- [Claude Code](https://claude.com/claude-code)（図を作らせる場合）

## 使い方

### Claude Code で図を作る

```
/create-diagram sequence 利用者が本を借りる流れ。…
/create-wireframe sc41 ledger 家計簿アプリの月次一覧画面。… pc と sp
```

どちらのコマンドも、次の順に進みます。

1. 図に必要な要素と、不明点を一覧にして、確認を求める（ここで止まる）
2. 確認が取れたら、スキルのルールに従って `.drawio` を作る
3. チェックを通し、画像に書き出して、結果を報告する

`review/` への反映とコミットは、頼んだときだけ行います。

### 画像に書き出す

```bash
# UML 図・ER 図（outputs/uml/svg/ に書き出す）
scripts/export_svg.sh                                  # 変更があった図だけ
scripts/export_svg.sh outputs/uml/drawio/er-study.drawio

# ワイヤーフレーム（ページごとに svg/ と png/ に書き出す）
scripts/export_wireframe.sh                            # 変更があった図だけ
scripts/export_wireframe.sh outputs/wireframes/drawio/wf-sc61-mypage.drawio
# → wf-sc61-mypage-pc.svg、wf-sc61-mypage-sp.svg、wf-sc61-mypage-sp-menu.svg など

# 部品カタログ（outputs/wireframes/catalog/ に書き出す）
scripts/export_wireframe.sh outputs/wireframes/catalog/catalog.drawio
```

どちらのスクリプトも、書き出す前にチェックを行い、ルール違反がある図は書き出しません。`-f` で、すべての図を書き出し直します。

## チェックの仕組み

Claude Code が `.drawio` を保存すると、hook（`.claude/hooks/check_drawio.py`）が自動でチェックします。置き場所で、チェックの内容が変わります。

| 置き場所 | 主なチェック |
| --- | --- |
| `outputs/uml/` | 非圧縮の XML か、図の種類ごとの接頭辞、線のつながり、矢印の種類など |
| `outputs/wireframes/drawio/` | ファイル名、ページ名と順番、画面枠の大きさ、8px グリッド、レイヤー（`frame`・`parts`・`notes`）、カタログにある図形だけを使っているか |
| `outputs/wireframes/catalog/` | ファイルの形式だけ |

見た目の確認（重なり、余白、注釈の位置など）は、書き出した PNG を見て行います。

## ワイヤーフレームのルール（要点）

詳しくは [.claude/skills/drawio-wireframe/references/rules.md](.claude/skills/drawio-wireframe/references/rules.md) にあります。

- ファイル名は `wf-<画面ID>-<名前>.drawio`。ページは `pc`、`sp` の順
- 別の状態は、`sp-menu` のように「-状態名」を付けたページを足す
- 部品の座標と大きさは 8 の倍数。余白は `pc` が 32、`sp` が 16
- 色はグレーと青だけを使う。赤は注釈（番号の丸と補足文）だけに使う
- 使える図形は、部品カタログ（[catalog.md](.claude/skills/drawio-wireframe/references/catalog.md)）の「採用」にあるものだけ
  - 新しい図形は、`catalog.drawio` で描画を確かめてから、採用の表に足す

## 作業の注意

- 既存の図は、指示がない限り上書きしません。修正版は、名前を変えて別のファイルにします
- `.drawio` は、作業中に VS Code の draw.io エディタで開かないでください（意図しない保存で、ファイルが壊れたり書式が変わったりします）
- `outputs/wireframes/png/` とカタログの画像は、作り直せるので git に入れません
