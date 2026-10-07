"""knowledge_index.py — 知识树查询、清单输出与依赖自检。

用法：
  python -B scripts/knowledge_index.py                 # 列全部叶
  python -B scripts/knowledge_index.py --leaf <id>     # 叶详情
  python -B scripts/knowledge_index.py --checklist <id>  # 输出评审清单
  python -B scripts/knowledge_index.py --check-deps    # deps.json 合规校验
"""
import json
import os
import sys

from _common import flag, leaf_ids, load_tree, skill_root

REQUIRED = ("name", "source_url", "license", "version", "install", "checked_at")


def list_leaves(tree):
    """打印叶索引。"""
    for leaf in tree.get("leaves", []):
        print("%-22s p=%s probes=%s" % (leaf.get("id"), leaf.get("priority"),
                                        ",".join(leaf.get("probes", []))))
    return 0


def show_leaf(tree, leaf_id):
    """打印单叶详情。"""
    for leaf in tree.get("leaves", []):
        if leaf.get("id") == leaf_id:
            print("title: %s" % leaf.get("title"))
            print("priority: %s" % leaf.get("priority"))
            print("knowledge: %s" % leaf.get("knowledge"))
            print("checklist: %s" % leaf.get("checklist"))
            print("cites: %s" % "\n       ".join(leaf.get("cites", [])))
            print("keywords: %s" % ", ".join(leaf.get("keywords", [])[:16]))
            return 0
    print("UNKNOWN_LEAF\t%s\t可选: %s" % (leaf_id, ", ".join(leaf_ids(tree))))
    return 4


def show_checklist(tree, leaf_id):
    """输出叶评审清单原文（供逐条勾选）。"""
    for leaf in tree.get("leaves", []):
        if leaf.get("id") == leaf_id:
            path = os.path.join(skill_root(), leaf.get("checklist", ""))
            if not os.path.exists(path):
                print("MISSING\t%s" % path)
                return 3
            with open(path, encoding="utf-8") as fh:
                sys.stdout.write(fh.read())
            return 0
    print("UNKNOWN_LEAF\t%s" % leaf_id)
    return 4


def check_deps():
    """校验 deps.json：每条须含全部字段且 source_url 为原始链接。"""
    path = os.path.join(skill_root(), "dependence", "deps.json")
    if not os.path.exists(path):
        print("MISSING\t%s" % path)
        return 3
    try:
        with open(path, encoding="utf-8") as fh:
            data = json.load(fh)
    except ValueError as exc:
        print("UNREADABLE\t%s" % exc)
        return 3
    bad = 0
    deps = data.get("dependencies", [])
    for dep in deps:
        name = dep.get("name", "<no-name>")
        missing = [k for k in REQUIRED if not dep.get(k)]
        url = dep.get("source_url", "")
        ok_url = url.startswith(("http://", "https://", "local://"))
        if missing or not ok_url:
            bad += 1
            print("BAD\t%s\tmissing=%s\turl=%s" % (name, missing, url or "-"))
    print("deps=%d bad=%d" % (len(deps), bad))
    return 1 if bad else 0


def main(argv):
    tree = load_tree()
    if tree is None:
        return 3
    if "--check-deps" in argv:
        return check_deps()
    leaf = flag(argv, "--leaf")
    if leaf:
        return show_leaf(tree, leaf)
    cl = flag(argv, "--checklist")
    if cl:
        return show_checklist(tree, cl)
    return list_leaves(tree)


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
