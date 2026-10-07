"""msix_probe.py — MSIX 包与依赖取证（含当前进程包标识）。

用法：
  python -B scripts/msix_probe.py                 # 已装包概览 + 包标识自检
  python -B scripts/msix_probe.py -PackageFamilyName <fn>   # 单包详情与依赖
  python -B scripts/msix_probe.py --deps          # 框架包依赖清单
非打包进程无包标识：需包标识的 API 会失败，须先本脚本实测再下结论。
"""
import sys

from _common import flag, has, lines_of, ps

IDENTITY = "$p = Get-AppxPackage -ErrorAction SilentlyContinue |"
IDENTITY += " Where-Object { $_.IsFramework -eq $false } | Select-Object -First 15;"
IDENTITY += " if ($p) { $p | ForEach-Object { $_.Name + ' ' + $_.Version +"
IDENTITY += " ' ' + $_.PackageFamilyName } } else { 'no-packages-or-side-by-side' }"

PKG = "Get-AppxPackage -PackageFamilyName '%s' -ErrorAction SilentlyContinue |"
PKG += " ForEach-Object { 'Name=' + $_.Name; 'Version=' + $_.Version;"
PKG += " 'InstallLocation=' + $_.InstallLocation; 'Dependencies=' + "
PKG += "($_.Dependencies.Name -join ',') }"

DEPS = "Get-AppxPackage -PackageTypeFilter Framework -ErrorAction SilentlyContinue |"
DEPS += " Select-Object -First 30 | ForEach-Object { $_.Name + ' ' + $_.Version }"

MANIFEST = "if (Test-Path '%s') { Get-Content '%s' -Raw } else { 'absent' }"


def emit(title, script, limit=30):
    """打印一段取证结果：0 有结果／3 不可用。"""
    print("== %s" % title)
    code, out = ps(script)
    if code is None or code != 0:
        print("  UNAVAILABLE\t%s" % (out or ""))
        return 3
    body = lines_of(out)
    for line in body[:limit]:
        print("  %s" % line)
    return 0 if body else 3


def main(argv):
    fam = flag(argv, "-PackageFamilyName") or flag(argv, "--family")
    if fam:
        return emit("包详情: %s" % fam, PKG % fam.replace("'", "''"))
    if has(argv, "--deps"):
        rc = emit("框架包依赖", DEPS)
        print("  判据：MSIX 安装失败常因框架包版本缺失，先比对再归因")
        return rc
    manifest = flag(argv, "--manifest")
    if manifest:
        path = manifest.replace("'", "''")
        return emit("清单内容: %s" % manifest, MANIFEST % (path, path))
    hits = 0
    hits += 1 if emit("已装应用包概览", IDENTITY) == 0 else 0
    hits += 1 if emit("框架包依赖", DEPS) == 0 else 0
    if hits == 0:
        print("降级：无 Appx 取证通道（如 LTSC/受限环境），打包判据标 [本地]")
        return 3
    print("提示：非打包桌面进程无包标识，ApplicationData 与后台任务通道不可用")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
