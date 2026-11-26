"""ワイヤーフレーム（outputs/wireframes/ の .drawio）のチェック

check_drawio.py から呼ばれる。UML 用のチェック（接頭辞、線の連結、矢印の種類など）は、
ワイヤーフレームには当てはまらないため、ここで別に定義する。

ルールの本体は .claude/skills/drawio-wireframe/references/rules.md。
ここでは、機械的に確かめられるものだけを検査する。

  - outputs/wireframes/drawio/ の .drawio … すべての項目を検査する
  - outputs/wireframes/catalog/ の .drawio（部品カタログ）… ファイルの形式だけを検査する
"""
import os
import re
import xml.etree.ElementTree as ET

# ページ名の先頭（版）→ 画面枠の大きさ（幅, 高さ）
SCREEN_SIZES = {"pc": (1280, 800), "sp": (375, 812)}
PAGE_ORDER = ["pc", "sp"]
# ページ名は、版（pc / sp）に、必要なら「-状態名」を付ける（例：sp-menu、pc-dialog）
PAGE_NAME_PATTERN = re.compile(r"^(pc|sp)(-[a-z0-9]+)*$")
REQUIRED_LAYERS = ["frame", "parts", "notes"]
FILE_NAME_PATTERN = re.compile(r"^wf-[a-z0-9]+-[a-z0-9]+(-[a-z0-9]+)*\.drawio$")

# 部品の採用リスト（図形名）は、カタログの「採用」の表を、そのまま読む
CATALOG_PATH = os.path.join(
    os.path.dirname(os.path.abspath(__file__)),
    "..", "skills", "drawio-wireframe", "references", "catalog.md",
)


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


def is_catalog(path):
    """部品カタログ（outputs/wireframes/catalog/）のファイルなら True"""
    parts = os.path.abspath(path).split(os.sep)
    return any(a == "wireframes" and b == "catalog" for a, b in zip(parts, parts[1:]))


def adopted_shapes():
    """カタログの「採用」の表にある図形名の集合。読めないときは None"""
    try:
        with open(CATALOG_PATH, encoding="utf-8") as f:
            text = f.read()
    except OSError:
        return None
    start = text.find("## 採用")
    end = text.find("## 不採用")
    if start < 0 or end < 0 or end < start:
        return None
    return set(re.findall(r"`mxgraph\.mockup\.([A-Za-z0-9_.]+)`", text[start:end]))


def page_base(name):
    """ページ名の版（pc / sp）。不正な名前なら None"""
    m = PAGE_NAME_PATTERN.match(name or "")
    return m.group(1) if m else None


def page_order_key(name):
    """並び順：pc の系統が先、sp の系統が後。同じ系統では、状態名のないページが先"""
    return (PAGE_ORDER.index(page_base(name)), 0 if name == page_base(name) else 1)


def is_multiple_of_8(value):
    return abs(value - round(value / 8) * 8) < 1e-6


def basic_check(root):
    """ファイルの形式のチェック。問題があれば、(エラー一覧, None)、なければ ([], 各ページの mxGraphModel)"""
    if root.tag != "mxfile":
        return ["ルート要素が <mxfile> ではありません"], None
    diagrams = root.findall("./diagram")
    models = [(d, d.find("mxGraphModel")) for d in diagrams]
    if not models or any(m is None for _, m in models):
        return ["<diagram> の中に <mxGraphModel> がありません（圧縮して保存されている可能性があります。非圧縮の XML で保存してください）"], None
    errors = []
    for d, m in models:
        if m.get("background", "").upper() != "#FFFFFF":
            errors.append(f'ページ {d.get("name")}: <mxGraphModel> に background="#FFFFFF" がありません')
    return errors, models


def check(path):
    """違反の内容を文字列のリストで返す。問題がなければ空のリスト"""
    try:
        root = ET.parse(path).getroot()
    except ET.ParseError as e:
        return [f"XML として読めません: {e}"]

    errors, models = basic_check(root)
    if models is None or is_catalog(path):
        return errors

    # --- ファイル名 ---
    name = os.path.basename(path)
    if not FILE_NAME_PATTERN.match(name):
        errors.append(f"ファイル名 {name} が `wf-<画面ID>-<名前>.drawio`（英小文字・数字・ハイフン）になっていません")

    # --- ページ名 ---
    page_names = [d.get("name") for d, _ in models]
    for pn in page_names:
        if page_base(pn) is None:
            errors.append(f"ページ名 {pn!r} は使えません（pc か sp。状態を描くときは sp-menu のように「-状態名」を付けてください）")
    if len(set(page_names)) != len(page_names):
        errors.append(f"ページ名が重複しています: {page_names}")
    known = [p for p in page_names if page_base(p)]
    if known != sorted(known, key=page_order_key):
        errors.append("ページの順番は、pc、pc-状態名、sp、sp-状態名 にしてください")

    catalog = adopted_shapes()
    if catalog is None:
        errors.append("部品カタログ（.claude/skills/drawio-wireframe/references/catalog.md）の「採用」の表が読めないため、図形名を確かめられません")
    for d, model in models:
        # ページ名が不正なページは、画面枠の大きさを決められないので、ページ名のエラーだけにする
        if page_base(d.get("name")):
            errors += check_page(d.get("name"), model, catalog)
    return errors


def check_page(page, model, catalog):
    errors = []
    cells = list(model.iter("mxCell"))
    by_id = {c.get("id"): c for c in cells}

    # --- レイヤー（parent="0" の mxCell のうち、図形でも線でもないもの）---
    layers = [c for c in cells if c.get("parent") == "0" and c.get("vertex") != "1" and c.get("edge") != "1"]
    layer_ids = {c.get("id") for c in layers}
    named = [(c.get("id"), c.get("value", "")) for c in layers if c.get("value")]
    names = [v for _, v in named]
    if names != REQUIRED_LAYERS:
        errors.append(
            f"ページ {page}: レイヤーは、下から順に {', '.join(REQUIRED_LAYERS)} の 3 つにしてください（今は {', '.join(names) or 'なし'}）"
        )

    def layer_of(cell):
        seen = set()
        while cell is not None and cell.get("id") not in seen:
            seen.add(cell.get("id"))
            parent = cell.get("parent")
            if parent in layer_ids:
                return parent
            cell = by_id.get(parent)
        return None

    # --- 部品ごとのチェック ---
    screen_found = False
    frame_h = None
    expected = SCREEN_SIZES.get(page_base(page))
    for c in cells:
        if c.get("vertex") != "1" and c.get("edge") != "1":
            continue
        cid = c.get("id")
        if layer_of(c) is None:
            errors.append(f"ページ {page}: 部品 {cid} が、frame・parts・notes のどのレイヤーにも属していません（既定のレイヤーに置かないでください）")
        if c.get("vertex") != "1":
            continue

        geo = c.find("mxGeometry")
        if geo is None:
            continue
        try:
            x, y = float(geo.get("x", "0")), float(geo.get("y", "0"))
            w, h = float(geo.get("width", "0")), float(geo.get("height", "0"))
        except ValueError:
            errors.append(f"ページ {page}: 部品 {cid} の座標が数値ではありません")
            continue

        # 画面枠（左上が (0, 0)、規定の幅で、高さは規定以上）は、8 の倍数の対象外
        if expected and (x, y, w) == (0, 0, expected[0]) and h >= expected[1]:
            screen_found = True
            frame_h = h
            continue

        # 画面の幅いっぱいの部品（ヘッダーなど）は幅が、高さいっぱいの部品（開いたメニューなど）は高さが、
        # 8 の倍数でなくてもよい
        full_width = expected and x == 0 and w == expected[0]
        full_height = expected and y == 0 and h == expected[1]
        checks = (("x", x), ("y", y), ("幅", w), ("高さ", h))
        bad = [f"{k}={v:g}" for k, v in checks
               if not is_multiple_of_8(v) and not (k == "幅" and full_width) and not (k == "高さ" and full_height)]
        if bad:
            errors.append(f"ページ {page}: 部品 {cid} が 8 の倍数ではありません（{', '.join(bad)}）")

        style = parse_style(c.get("style"))
        shape = style.get("shape", "")
        # mainText が数字だけだと、draw.io の書き出しが失敗する（全角の数字なら書き出せる）
        if shape.startswith("mxgraph.mockup.") and re.fullmatch(r"[0-9.+-]+", style.get("mainText", "")):
            errors.append(
                f"ページ {page}: 部品 {cid} の mainText={style['mainText']} は、数字だけのため書き出しに失敗します"
                "（全角の数字にするか、文字を足してください）"
            )
        if shape.startswith("mxgraph.mockup.") and catalog is not None:
            if shape[len("mxgraph.mockup."):] not in catalog:
                errors.append(f"ページ {page}: 部品 {cid} の図形 {shape} は、カタログの採用リストにありません")

    if expected and not screen_found:
        errors.append(f"ページ {page}: 画面枠（左上 (0, 0)、幅 {expected[0]}、高さ {expected[1]} 以上の四角形）がありません")
    elif expected and frame_h > expected[1] and not has_fold_line(cells, layer_of, expected[1]):
        errors.append(
            f"ページ {page}: 画面枠を {expected[1]} より高くした場合は、y={expected[1]} の位置に、"
            "画面の下端を示す点線（frame レイヤーの線）を引いてください"
        )
    return errors


def has_fold_line(cells, layer_of, y_fold):
    """frame レイヤーに、y=y_fold を水平に通る線（sourcePoint と targetPoint の y が同じ）があるか"""
    for c in cells:
        if c.get("edge") != "1" or not layer_of(c) or not layer_of(c).startswith("layer-frame"):
            continue
        geo = c.find("mxGeometry")
        pts = {p.get("as"): p.get("y") for p in geo.findall("mxPoint")} if geo is not None else {}
        try:
            if float(pts["sourcePoint"]) == float(pts["targetPoint"]) == y_fold:
                return True
        except (KeyError, TypeError, ValueError):
            continue
    return False
