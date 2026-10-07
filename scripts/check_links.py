"""check_links.py — 悬空链接与 .md 行数自检（红线：悬空必须为 0，.md ≤ 50 行）。

用法：python -B scripts/check_links.py --root .
检查项：
  1) markdown 相对链接目标是否存在（跳过 http(s)/local:// 与锚点外链）；
  2) 每个 .md 行数是否 ≤ 50；
  3) scripts/ 内每个 .py 是否真实存在且可编译。
"""
import os
import re
import sys

from _common import flag

LINK = re.compile(r"\[[^\]]*\]\(([^)]+)\)")
MAX_LINES = 50
SKIP = ("http://", "https://", "local://", "mailto:", "#")


def iter_md(root):
    """遍历技能目录内的 .md 文件（跳过 tmp 与 .git）。"""
    for dirpath, dirnames, filenames in os.walk(root):
        dirnames[:] = [d for d in dirnames if d not in ("tmp", ".git",
                                                       "__pycache__")]
        for name in filenames:
            if name.endswith(".md"):
                yield os.path.join(dirpath, name)


def check_file(path):
    """返回 (悬空链接列表, 行数超限标志)。"""
    with open(path, encoding="utf-8") as fh:
        text = fh.read()
    lines = text.splitlines()
    base = os.path.dirname(path)
    dangling = []
    for target in LINK.findall(text):
        clean = target.split("#")[0].strip()
        if not clean or clean.startswith(SKIP):
            continue
        resolved = os.path.normpath(os.path.join(base, clean))
        if not os.path.exists(resolved):
            dangling.append(target)
    return dangling, len(lines) > MAX_LINES


def check_scripts(root):
    """scripts/ 内 .py 文件须存在且可编译。"""
    bad = []
    folder = os.path.join(root, "scripts")
    if not os.path.isdir(folder):
        return ["scripts/ 目录缺失"]
    for name in sorted(os.listdir(folder)):
        if not name.endswith(".py"):
            continue
        path = os.path.join(folder, name)
        try:
            with open(path, encoding="utf-8") as fh:
                compile(fh.read(), path, "exec")
        except SyntaxError as exc:
            bad.append("%s: %s" % (name, exc))
    return bad


def main(argv):
    root = flag(argv, "--root") or "."
    root = os.path.abspath(root)
    problems = 0
    for path in sorted(iter_md(root)):
        dangling, too_long = check_file(path)
        rel = os.path.relpath(path, root)
        for target in dangling:
            print("DANGLING\t%s -> %s" % (rel, target))
            problems += 1
        if too_long:
            print("TOO_LONG\t%s (> %d 行)" % (rel, MAX_LINES))
            problems += 1
    for bad in check_scripts(root):
        print("SCRIPT\t%s" % bad)
        problems += 1
    print("checked_root=%s problems=%d" % (root, problems))
    return 1 if problems else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
