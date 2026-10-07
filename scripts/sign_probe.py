"""sign_probe.py — Authenticode 签名与证书链校验取证。

用法：
  python -B scripts/sign_probe.py -Path <文件>     # 单文件签名状态
  python -B scripts/sign_probe.py --store          # 当前用户证书概览（不含私钥）
  python -B scripts/sign_probe.py --dir <目录>     # 目录内 exe/dll 批量签名核查
禁止凭空假设目标机有可用证书：结论只来自本脚本实测输出。
"""
import sys

from _common import flag, has, lines_of, ps

SINGLE = "$s = Get-AuthenticodeSignature -FilePath '%s';"
SINGLE += "'Status=' + $s.Status; 'Signer=' + $s.SignerCertificate.Subject;"
SINGLE += "'Thumbprint=' + $s.SignerCertificate.Thumbprint;"
SINGLE += "'NotAfter=' + $s.SignerCertificate.NotAfter;"
SINGLE += "'HasTimestamp=' + [bool]$s.TimeStamp; 'StatusMessage=' + $s.StatusMessage"

STORE = "Get-ChildItem Cert:\\CurrentUser\\My -ErrorAction SilentlyContinue |"
STORE += " ForEach-Object { $_.Thumbprint + ' ' + $_.NotAfter.ToString('yyyy-MM-dd')"
STORE += " + ' ' + $_.Subject }"

BATCH = "Get-ChildItem -Path '%s' -Include *.exe,*.dll -Recurse -ErrorAction"
BATCH += " SilentlyContinue | Select-Object -First 40 | ForEach-Object {"
BATCH += " $s = Get-AuthenticodeSignature $_.FullName;"
BATCH += " $s.Status.ToString() + ' ' + $_.Name }"


def emit(title, script):
    """打印一段取证结果。"""
    print("== %s" % title)
    code, out = ps(script)
    if code is None or code != 0:
        print("  UNAVAILABLE\t%s" % (out or "powershell 不可用"))
        return 3
    for line in lines_of(out)[:40]:
        print("  %s" % line)
    return 0


def main(argv):
    target = flag(argv, "-Path") or flag(argv, "--path")
    if target:
        return emit("签名状态: %s" % target, SINGLE % target.replace("'", "''"))
    if has(argv, "--store"):
        print("提示：只列公开证书信息，不导出私钥；私钥可用性须现场验证")
        return emit("当前用户个人证书存储", STORE)
    folder = flag(argv, "--dir")
    if folder:
        return emit("目录批量核查: %s" % folder, BATCH % folder.replace("'", "''"))
    print("用法: sign_probe.py -Path <文件> | --store | --dir <目录>")
    print("判据：Status=Valid 且 HasTimestamp=True 才可断言「签名长期有效」")
    return 2


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
