#!/usr/bin/env python3
"""draw.io (.drawio) のチェックスクリプト

使い方
  hook から  : 標準入力で Claude Code の JSON を受け取り、書き込まれたファイルを検査する
  手動で実行 : python3 .claude/hooks/check_drawio.py docs/diagrams/er-study.drawio ...

終了コード
  0 … 問題なし（または .drawio 以外のファイル）
  2 … ルール違反あり。内容は標準エラー出力に出す（hook では Claude Code に返される）

チェック項目は、これまでのレビューで実際に起きた失敗に対応するものだけにしている。
"""
import json
import os
import re
import sys
import xml.etree.ElementTree as ET

# ファイル名の接頭辞 → 図の種類
PREFIXES = ["usecase", "class", "sequence", "activity", "state", "er", "screen"]


def parse_style(style):
    """'a=1;b=2;text;' を {'a': '1', 'b': '2', 'text': ''} に変換する"""
    result = {}
    for part in (style or "").split(";"):
        part = part.strip()
        if not part:
            continue
        if "=" in part:
            k, v = part.split("=", 1)
            result[k.strip()] = v.strip()
        else:
            result[part] = ""
    return result


def plain_text(value):
    """HTML のタグと実体参照を除いた文字列を返す"""
    text = re.sub(r"<[^>]*>", "", value or "")
    text = text.replace("&nbsp;", " ")
    return text.strip()


def end_arrow(style):
    # draw.io は endArrow を省略すると classic（塗りつぶし）になる
    return style.get("endArrow", "classic"), style.get("endFill", "1")


def diagram_type(path):
    name = os.path.basename(path)
    for p in PREFIXES:
        if name.startswith(p + "-"):
            return p
    return None


def check(path):
    errors = []
    kind = diagram_type(path)
    if kind is None:
        errors.append(
            "ファイル名が `<種類>-<名前>.drawio` になっていません。"
            f"種類は {', '.join(PREFIXES)} のどれかにしてください"
        )

    try:
        root = ET.parse(path).getroot()
    except ET.ParseError as e:
        return [f"XML として読めません: {e}"]

    # --- ファイル全体の設定 ---
    if root.tag != "mxfile":
        return ["ルート要素が <mxfile> ではありません"]
    if root.get("scale") != "1":
        errors.append('<mxfile> に scale="1" がありません')
    if root.get("border") != "20":
        errors.append('<mxfile> に border="20" がありません')

    models = root.findall("./diagram/mxGraphModel")
    if not models:
        return errors + ["<diagram> の中に <mxGraphModel> がありません（圧縮して保存されている可能性があります。非圧縮の XML で保存してください）"]

    for model in models:
        if model.get("background", "").upper() != "#FFFFFF":
            errors.append('<mxGraphModel> に background="#FFFFFF" がありません')

        cells = list(model.iter("mxCell"))
        ids = {c.get("id") for c in cells}
        vertices = [c for c in cells if c.get("vertex") == "1"]
        edges = [c for c in cells if c.get("edge") == "1"]

        # --- 共通：線の連結 ---
        for e in edges:
            eid = e.get("id")
            src, tgt = e.get("source"), e.get("target")
            if kind == "sequence":
                # シーケンス図のメッセージは連結しない。座標で指定する
                geo = e.find("mxGeometry")
                points = {p.get("as") for p in geo.findall("mxPoint")} if geo is not None else set()
                if not (src and tgt) and not {"sourcePoint", "targetPoint"} <= points:
                    errors.append(f"線 {eid}: source/target も sourcePoint/targetPoint もありません")
                continue
            if not src or not tgt:
                errors.append(f"線 {eid}: source または target がありません（端点が図形に連結されていません）")
            for ref in (src, tgt):
                if ref and ref not in ids:
                    errors.append(f"線 {eid}: 存在しない図形 {ref} を参照しています")

        # --- 図の種類ごとのチェック ---
        if kind == "sequence":
            errors += check_sequence(vertices, edges, cells)
        elif kind in ("activity", "state", "screen"):
            for e in edges:
                arrow, fill = end_arrow(parse_style(e.get("style")))
                if arrow != "open" or fill != "0":
                    errors.append(
                        f"線 {e.get('id')}: 矢印は開いた矢印（endArrow=open;endFill=0）にしてください"
                        f"（今は endArrow={arrow};endFill={fill}）"
                    )
        elif kind == "er":
            errors += check_er(edges)

    return errors


def check_sequence(vertices, edges, cells):
    errors = []

    # アクターの名前と棒人間の重なり
    for v in vertices:
        s = parse_style(v.get("style"))
        if "umlLifeline" in s.get("shape", "") and s.get("participant") == "umlActor":
            size = float(s.get("size", "40"))
            spacing = float(s.get("spacingTop", "0"))
            if s.get("verticalAlign") != "top" or spacing <= size:
                errors.append(
                    f"アクター {v.get('id')}: verticalAlign=top を付け、spacingTop を size より大きくしてください"
                    f"（今は size={size:g}, spacingTop={spacing:g}）"
                )

    # メッセージの矢印の種類と、y 座標の重複
    seen_y = {}
    for e in edges:
        s = parse_style(e.get("style"))
        arrow, fill = end_arrow(s)
        if s.get("dashed") == "1":
            if arrow != "open" or fill != "0":
                errors.append(f"線 {e.get('id')}: 戻り値は点線＋開いた矢印（endArrow=open;endFill=0）にしてください")
        else:
            if arrow != "block" or fill != "1":
                errors.append(f"線 {e.get('id')}: 呼び出しは実線＋塗りつぶしの三角（endArrow=block;endFill=1）にしてください")

        geo = e.find("mxGeometry")
        if geo is not None:
            for p in geo.findall("mxPoint"):
                if p.get("as") == "sourcePoint" and p.get("y") is not None:
                    y = p.get("y")
                    if y in seen_y:
                        errors.append(f"線 {e.get('id')} と {seen_y[y]}: 同じ y={y} にあります。メッセージは y をずらしてください")
                    else:
                        seen_y[y] = e.get("id")

    # alt などの枠は最前面（XML の最後のほう）に置く
    order = {c.get("id"): i for i, c in enumerate(cells)}
    frames = [v for v in vertices if "umlFrame" in parse_style(v.get("style")).get("shape", "")]
    others = [v for v in vertices if v not in frames]
    for f in frames:
        later = [o.get("id") for o in others if order[o.get("id")] > order[f.get("id")]]
        if later:
            errors.append(f"枠 {f.get('id')}: XML でほかの図形（{', '.join(later[:3])} など）より後に書き、最前面にしてください")
    return errors


def check_er(edges):
    errors = []
    child_arrows = {"ERzeroToMany", "ERoneToMany", "ERzeroToOne"}
    for e in edges:
        s = parse_style(e.get("style"))
        eid = e.get("id")
        if s.get("startArrow") != "ERmandOne":
            errors.append(f"線 {eid}: 親側（source）は startArrow=ERmandOne にしてください")
        if s.get("endArrow") not in child_arrows:
            errors.append(f"線 {eid}: 子側（target）は endArrow を {' / '.join(sorted(child_arrows))} のどれかにしてください")
        if not plain_text(e.get("value")):
            errors.append(f"線 {eid}: リレーション名のラベルがありません")
    return errors


def targets_from_hook():
    """hook から呼ばれたとき、書き込まれたファイルのパスを返す"""
    try:
        data = json.load(sys.stdin)
    except (json.JSONDecodeError, ValueError):
        return []
    path = (data.get("tool_input") or {}).get("file_path")
    return [path] if path else []


def main():
    paths = sys.argv[1:] or targets_from_hook()
    # 対象は .drawio だけ（.drawio.svg や .drawio.png は対象外）
    paths = [p for p in paths if p.endswith(".drawio") and os.path.isfile(p)]

    failed = False
    for p in paths:
        errors = check(p)
        if errors:
            failed = True
            print(f"[check_drawio] {p} にルール違反があります（{len(errors)} 件）。直してください:", file=sys.stderr)
            for msg in errors:
                print(f"  - {msg}", file=sys.stderr)
        elif sys.argv[1:]:
            print(f"[check_drawio] {p}: OK")
    sys.exit(2 if failed else 0)


if __name__ == "__main__":
    main()
