"""classify_topic.py — 关键词命中计分，把问题映射到知识树叶。

用法：python -B scripts/classify_topic.py -q "应用在高 DPI 屏上模糊"
数据源：asset/knowledge_tree.json（唯一数据源，禁止在此硬编码叶）。
"""
import sys

from _common import flag, leaf_ids, load_tree


def score(tree, text):
    """返回 [(叶id, 命中数, 命中词列表)]，按命中数与优先级排序。"""
    low = text.lower()
    hits = []
    for leaf in tree.get("leaves", []):
        found = [kw for kw in leaf.get("keywords", [])
                 if kw.lower() in low]
        if found:
            hits.append((leaf.get("id", ""), len(found), found,
                         leaf.get("priority", 9)))
    hits.sort(key=lambda item: (-item[1], item[3]))
    return hits


def main(argv):
    query = flag(argv, "-q") or flag(argv, "--query")
    if not query:
        query = " ".join(a for a in argv if not a.startswith("-"))
    if not query.strip():
        print("用法: classify_topic.py -q \"<问题文本>\"")
        return 2
    tree = load_tree()
    if tree is None:
        return 3
    hits = score(tree, query)
    if not hits:
        print("NO_LEAF\t范围外：转派（Qt/Web/语言级见 dependence/dependence.md）")
        print("叶清单: %s" % ", ".join(leaf_ids(tree)))
        return 4
    for leaf_id, count, words, prio in hits[:3]:
        print("%-22s score=%d priority=%d\t%s" % (leaf_id, count, prio,
                                                  ", ".join(words[:8])))
    print("建议取证探针: %s" % ", ".join(
        sorted({p for lf in tree.get("leaves", [])
                if lf.get("id") in [h[0] for h in hits[:3]]
                for p in lf.get("probes", [])})))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
