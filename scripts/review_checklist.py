"""review_checklist.py — 生成叶评审清单的填写模板并统计勾选结果。

用法：
  python -B scripts/review_checklist.py --leaf <叶id>       # 输出待填模板
  python -B scripts/review_checklist.py --leaf <id> --filled <文件>  # 统计
与 knowledge_index.py --checklist 的差别：本脚本产出「证据列」模板并做计数。
"""
import os
import re
import sys

from _common import flag, leaf_ids, load_tree, skill_root

ITEM = re.compile(r"^\s*-\s*\[( |x|X)\]\s*(.*)$")


def template(tree, leaf_id):
    """把叶清单转成「判据 | 证据 | 结论」三列模板。"""
    for leaf in tree.get("leaves", []):
        if leaf.get("id") != leaf_id:
            continue
        path = os.path.join(skill_root(), leaf.get("checklist", ""))
        if not os.path.exists(path):
            print("MISSING\t%s" % path)
            return None
        with open(path, encoding="utf-8") as fh:
            return [ln.rstrip() for ln in fh]
    print("UNKNOWN_LEAF\t%s\t可选: %s" % (leaf_id, ", ".join(leaf_ids(tree))))
    return None


def count(lines):
    """统计勾选与级别分布。"""
    total = passed = 0
    levels = {}
    for line in lines:
        match = ITEM.match(line)
        if not match:
            continue
        total += 1
        checked = match.group(1).lower() == "x"
        passed += 1 if checked else 0
        level = match.group(2).split("|")[0].strip()
        levels[level] = levels.get(level, 0) + (0 if checked else 1)
    return total, passed, levels


def main(argv):
    tree = load_tree()
    if tree is None:
        return 3
    leaf = flag(argv, "--leaf")
    if not leaf:
        print("用法: review_checklist.py --leaf <叶id> [--filled <文件>]")
        print("叶: %s" % ", ".join(leaf_ids(tree)))
        return 2
    filled = flag(argv, "--filled")
    if filled:
        if not os.path.exists(filled):
            print("MISSING\t%s" % filled)
            return 3
        with open(filled, encoding="utf-8") as fh:
            lines = fh.read().splitlines()
    else:
        lines = template(tree, leaf)
        if lines is None:
            return 4
        print("填写规则：勾选 [x] 表示通过；每条须补「证据」列（命令输出行或文档条目）")
        return 0
    total, passed, levels = count(lines)
    print("leaf=%s total=%d passed=%d unchecked=%d" % (leaf, total, passed,
                                                       total - passed))
    for level, num in sorted(levels.items()):
        print("  未通过 %-9s %d" % (level, num))
    if total == 0:
        print("NO_ITEMS\t清单为空或格式不符（须为 `- [ ] 级别 | 判据 | 出处`）")
        return 4
    return 0 if passed == total else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
