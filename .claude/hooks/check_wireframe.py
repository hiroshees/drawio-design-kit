"""ワイヤーフレーム（outputs/wireframes/ の .drawio）のチェック

check_drawio.py から呼ばれる。UML 用のチェック（接頭辞、線の連結、矢印の種類など）は、
ワイヤーフレームには当てはまらないため、ここで別に定義する。

今は「ファイルとして壊れていないか」だけを見る。画面サイズ・余白・名前の付け方などは、
ルールが決まったあと（フェーズ 2〜3）に、機械的に確かめられるものを追加する。
"""
import xml.etree.ElementTree as ET


def check(path):
    """違反の内容を文字列のリストで返す。問題がなければ空のリスト"""
    try:
        root = ET.parse(path).getroot()
    except ET.ParseError as e:
        return [f"XML として読めません: {e}"]

    if root.tag != "mxfile":
        return ["ルート要素が <mxfile> ではありません"]

    models = root.findall("./diagram/mxGraphModel")
    if not models:
        return ["<diagram> の中に <mxGraphModel> がありません（圧縮して保存されている可能性があります。非圧縮の XML で保存してください）"]

    errors = []
    for model in models:
        if model.get("background", "").upper() != "#FFFFFF":
            errors.append('<mxGraphModel> に background="#FFFFFF" がありません')
    return errors
