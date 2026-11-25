#!/usr/bin/env bash
# draw.io の図（.drawio）を SVG に書き出す
#
# 使い方
#   scripts/export_svg.sh                 … 変更があった図だけ書き出す
#   scripts/export_svg.sh -f              … すべての図を書き出し直す
#   scripts/export_svg.sh ファイル...      … 指定した図だけ書き出す（変更の有無に関係なく）
#
# 動き
#   - 入力：outputs/uml/drawio/*.drawio
#   - 出力：outputs/uml/svg/<同じ名前>.svg（例：er-study.drawio → er-study.svg）
#   - 書き出す前に check_drawio.py でチェックし、ルール違反がある図は書き出さない
#   - 図のコピーは埋め込まない（-e を付けない）。余白は 20px
#
# 終了コード
#   0 … すべて成功（またはスキップ）
#   1 … チェック違反や書き出しの失敗が 1 件以上ある

set -u

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
SRC_DIR="$ROOT/outputs/uml/drawio"
OUT_DIR="$ROOT/outputs/uml/svg"
CHECKER="$ROOT/.claude/hooks/check_drawio.py"
BORDER=20

force=0
files=()
for arg in "$@"; do
  case "$arg" in
    -f|--force) force=1 ;;
    -h|--help) sed -n '2,19p' "$0"; exit 0 ;;
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

mkdir -p "$OUT_DIR"

exported=0; skipped=0; failed=0
for src in "${files[@]}"; do
  if [[ "$src" != *.drawio ]] || [ ! -f "$src" ]; then
    echo "NG    $src（.drawio のファイルではありません）"
    failed=$((failed + 1)); continue
  fi

  name="$(basename "$src" .drawio)"
  out="$OUT_DIR/$name.svg"

  # 変更がなければスキップ（SVG のほうが新しい場合）
  if [ "$force" -eq 0 ] && [ -f "$out" ] && [ "$out" -nt "$src" ]; then
    echo "SKIP  $name（変更なし）"
    skipped=$((skipped + 1)); continue
  fi

  # チェックに通らない図は書き出さない
  if ! check_msg="$(python3 "$CHECKER" "$src" 2>&1)"; then
    echo "NG    $name（チェック違反のため書き出しません）"
    echo "$check_msg" | sed 's/^/      /'
    failed=$((failed + 1)); continue
  fi

  # 書き出し。draw.io の警告（dbus や GPU など）は、失敗したときだけ表示する
  # 一時フォルダに書き出してから移す（失敗したときに、前の SVG を壊さないため）
  tmp="$(mktemp -d)"
  log="$tmp/drawio.log"
  if "${runner[@]}" drawio -x -f svg -b "$BORDER" -o "$tmp/$name.svg" "$src" >"$log" 2>&1 && [ -s "$tmp/$name.svg" ]; then
    mv "$tmp/$name.svg" "$out"
    echo "OK    $name → ${out#$ROOT/}"
    exported=$((exported + 1))
  else
    echo "NG    $name（書き出しに失敗しました）"
    sed 's/^/      /' "$log"
    failed=$((failed + 1))
  fi
  rm -rf "$tmp"
done

echo "----"
echo "書き出し: $exported 件 / スキップ: $skipped 件 / 失敗: $failed 件"
[ "$failed" -eq 0 ]
