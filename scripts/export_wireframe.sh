#!/usr/bin/env bash
# ワイヤーフレームの図（.drawio）を、ページごとに SVG と PNG に書き出す
#
# 使い方
#   scripts/export_wireframe.sh                 … 変更があった図だけ書き出す
#   scripts/export_wireframe.sh -f              … すべての図を書き出し直す
#   scripts/export_wireframe.sh ファイル...      … 指定した図だけ書き出す（変更の有無に関係なく）
#
# 動き
#   - 入力：outputs/wireframes/drawio/*.drawio（1 ファイルに pc と sp など複数のページがある）
#   - 出力：ページごとに別のファイル
#           outputs/wireframes/svg/<ファイル名>-<ページ名>.svg（表示用）
#           outputs/wireframes/png/<ファイル名>-<ページ名>.png（Claude Code が見た目を確認する用）
#           例：wf-sc01-login.drawio の pc ページ → wf-sc01-login-pc.svg / wf-sc01-login-pc.png
#   - 書き出す前に check_drawio.py でチェックし、ルール違反がある図は書き出さない
#   - 図のコピーは埋め込まない（-e を付けない）。余白は 20px、PNG の拡大率は等倍
#   - ページ名は、英数字・ハイフン・アンダースコアだけ使える（ファイル名にするため）
#   - UML 用の scripts/export_svg.sh とは別のスクリプト（そちらは変更しない）
#
# 終了コード
#   0 … すべて成功（またはスキップ）
#   1 … チェック違反や書き出しの失敗が 1 件以上ある

set -u

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
SRC_DIR="$ROOT/outputs/wireframes/drawio"
SVG_DIR="$ROOT/outputs/wireframes/svg"
PNG_DIR="$ROOT/outputs/wireframes/png"
CHECKER="$ROOT/.claude/hooks/check_drawio.py"
BORDER=20
PNG_SCALE=1

force=0
files=()
for arg in "$@"; do
  case "$arg" in
    -f|--force) force=1 ;;
    -h|--help) sed -n '2,22p' "$0"; exit 0 ;;
    *) files+=("$arg"); force=1 ;;   # ファイルを指定したときは、変更の有無に関係なく書き出す
  esac
done

if ! command -v drawio >/dev/null 2>&1; then
  echo "drawio コマンドが見つかりません。draw.io のデスクトップ版をインストールしてください" >&2
  exit 1
fi

# 画面のない環境では、xvfb-run があればそれを使う（WSLg がある環境では不要）
runner=()
if [ -z "${DISPLAY:-}" ] && [ -z "${WAYLAND_DISPLAY:-}" ] && command -v xvfb-run >/dev/null 2>&1; then
  runner=(xvfb-run -a)
fi

if [ ${#files[@]} -eq 0 ]; then
  shopt -s nullglob
  files=("$SRC_DIR"/*.drawio)
fi

mkdir -p "$SVG_DIR" "$PNG_DIR"

# .drawio のページ名を、1 行に 1 つ、先頭のページから順に出力する
list_pages() {
  python3 -I - "$1" <<'PY'
import sys
import xml.etree.ElementTree as ET
for d in ET.parse(sys.argv[1]).getroot().findall("diagram"):
    print(d.get("name", ""))
PY
}

exported=0; skipped=0; failed=0
for src in "${files[@]}"; do
  if [[ "$src" != *.drawio ]] || [ ! -f "$src" ]; then
    echo "NG    $src（.drawio のファイルではありません）"
    failed=$((failed + 1)); continue
  fi

  name="$(basename "$src" .drawio)"

  # チェックに通らない図は書き出さない
  if ! check_msg="$(python3 "$CHECKER" "$src" 2>&1)"; then
    echo "NG    $name（チェック違反のため書き出しません）"
    echo "$check_msg" | sed 's/^/      /'
    failed=$((failed + 1)); continue
  fi

  # ページ名の一覧を取る。名前が空、使えない文字を含む、重複している場合は書き出さない
  pages=()
  while IFS= read -r p; do pages+=("$p"); done < <(list_pages "$src")
  bad=""
  declare -A seen=()
  for p in "${pages[@]}"; do
    if [[ ! "$p" =~ ^[A-Za-z0-9_-]+$ ]]; then bad="ページ名「$p」は使えません（英数字・ハイフン・アンダースコアのみ）"; break; fi
    if [ -n "${seen[$p]:-}" ]; then bad="ページ名「$p」が重複しています"; break; fi
    seen[$p]=1
  done
  unset seen
  if [ ${#pages[@]} -eq 0 ] || [ -n "$bad" ]; then
    echo "NG    $name（${bad:-ページがありません}）"
    failed=$((failed + 1)); continue
  fi

  index=0
  for page in "${pages[@]}"; do
    index=$((index + 1))                # drawio の -p は 1 始まり
    out="$name-$page"
    svg="$SVG_DIR/$out.svg"
    png="$PNG_DIR/$out.png"

    # 変更がなければスキップ（SVG と PNG の両方が新しい場合）
    if [ "$force" -eq 0 ] && [ -f "$svg" ] && [ -f "$png" ] && [ "$svg" -nt "$src" ] && [ "$png" -nt "$src" ]; then
      echo "SKIP  $out（変更なし）"
      skipped=$((skipped + 1)); continue
    fi

    # 一時フォルダに書き出してから移す（失敗したときに、前のファイルを壊さないため）
    # draw.io の警告（dbus や GPU など）は、失敗したときだけ表示する
    tmp="$(mktemp -d)"
    log="$tmp/drawio.log"
    if "${runner[@]}" drawio -x -f svg -p "$index" -b "$BORDER" -o "$tmp/$out.svg" "$src" >"$log" 2>&1 && [ -s "$tmp/$out.svg" ] \
       && "${runner[@]}" drawio -x -f png -p "$index" -s "$PNG_SCALE" -b "$BORDER" -o "$tmp/$out.png" "$src" >>"$log" 2>&1 && [ -s "$tmp/$out.png" ]; then
      mv "$tmp/$out.svg" "$svg"
      mv "$tmp/$out.png" "$png"
      echo "OK    $out → ${svg#$ROOT/} , ${png#$ROOT/}"
      exported=$((exported + 1))
    else
      echo "NG    $out（書き出しに失敗しました）"
      sed 's/^/      /' "$log"
      failed=$((failed + 1))
    fi
    rm -rf "$tmp"
  done
done

echo "----"
echo "書き出し: $exported 件 / スキップ: $skipped 件 / 失敗: $failed 件（件数はページ単位）"
[ "$failed" -eq 0 ]
