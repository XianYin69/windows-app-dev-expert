"""_common.py — 探针共用工具：PowerShell 调用、参数解析、知识树读取。

本模块不含业务判断，仅供 scripts/ 内探针导入。
"""
import json
import os
import shutil
import subprocess
import sys

TIMEOUT = 40


def skill_root():
    """技能根目录（scripts/ 的上一级）。"""
    return os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def which(cmd):
    """返回可执行文件绝对路径或 None。"""
    return shutil.which(cmd)


def run(cmd, timeout=TIMEOUT):
    """执行命令列表，返回 (返回码, 合并输出)；缺可执行返回 (None, 'absent')。"""
    if not cmd or not which(cmd[0]):
        return None, "absent: %s" % cmd[0]
    try:
        proc = subprocess.run(cmd, capture_output=True, text=True,
                              errors="replace", timeout=timeout)
    except (subprocess.SubprocessError, OSError) as exc:
        return 128, "error: %s" % exc
    out = (proc.stdout or "") + (proc.stderr or "")
    return proc.returncode, out.strip()


def ps(script, timeout=TIMEOUT):
    """调用 Windows PowerShell 5.1（系统内置）执行只读取证脚本。"""
    exe = (os.path.join(os.environ.get("SystemRoot", r"C:\Windows"),
                        "System32", "WindowsPowerShell", "v1.0",
                        "powershell.exe"))
    if not os.path.exists(exe):
        exe = which("powershell")
    if not exe:
        return None, "absent: powershell"
    cmd = [exe, "-NoProfile", "-NonInteractive", "-ExecutionPolicy",
           "Bypass", "-Command", script]
    return run(cmd, timeout)


def lines_of(text):
    """非空输出行列表。"""
    return [ln.strip() for ln in text.splitlines() if ln.strip()]


def flag(argv, name, default=None):
    """取 --name value 形式的参数值。"""
    if name in argv:
        i = argv.index(name)
        if i + 1 < len(argv):
            return argv[i + 1]
    return default


def has(argv, name):
    """取 --name 开关。"""
    return name in argv


def load_tree(root=None):
    """读取 asset/knowledge_tree.json；缺失返回 None 并打印原因。"""
    path = os.path.join(root or skill_root(), "asset", "knowledge_tree.json")
    if not os.path.exists(path):
        print("MISSING\t%s" % path)
        return None
    try:
        with open(path, encoding="utf-8") as fh:
            return json.load(fh)
    except (OSError, ValueError) as exc:
        print("UNREADABLE\t%s\t%s" % (path, exc))
        return None


def leaf_ids(tree):
    """叶 id 列表。"""
    return [lf.get("id", "") for lf in tree.get("leaves", [])] if tree else []


def report(label, ok, detail=""):
    """统一单行报告格式。"""
    print("%-18s %s\t%s" % (label, "FOUND" if ok else "ABSENT", detail))
    return 1 if ok else 0
