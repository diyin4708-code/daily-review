#!/usr/bin/env python3
"""
每日三省吾身 — 10:00 / 16:00 / 22:00
"""

import subprocess, os, time
from datetime import datetime

LOG_FILE = os.path.expanduser("~/.openclaw/workspace/daily_check.log")
MEMORY_DIR = os.path.expanduser("~/.openclaw/workspace/memory/")
MEMORY_FILE = MEMORY_DIR + datetime.now().strftime("%Y-%m-%d") + ".md"
UNDICI_TARGET = os.path.expanduser("~/.npm-global/lib/node_modules/openclaw/node_modules/undici")
UNDICI_SOURCE = "/home/openclaw/.npm-global/lib/node_modules/clawhub/node_modules/undici"  # 7.25 版

def log(msg):
    t = datetime.now().strftime("%H:%M:%S")
    line = f"[{t}] {msg}"
    print(line)
    os.makedirs(os.path.dirname(LOG_FILE), exist_ok=True)
    with open(LOG_FILE, "a") as f: f.write(line + "\n")

def run(cmd, timeout=5):
    try:
        r = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=timeout)
        return r.stdout.strip(), r.returncode
    except: return "", 1

def check_undici():
    out, _ = run(f"node -e \"console.log(require('{UNDICI_TARGET}/package.json').version)\"")
    if out == "7.25.0": return True, out
    log(f"⚠️ undici={out}, 修复中...")
    run(f"rm -rf {UNDICI_TARGET}")
    run(f"cp -r {UNDICI_SOURCE} {UNDICI_TARGET}")
    return False, out

def check_proxy():
    out, _ = run("curl -s --max-time 3 http://172.19.208.1:7897")
    return out != ""

def check_telegram():
    out, _ = run("grep -oP 'botToken\":\\s*\"[^\"]+' ~/.openclaw/openclaw.json")
    token = out.split('"')[-1] if out else ""
    if not token: return False
    import urllib.request
    try:
        req = urllib.request.Request(f"https://api.telegram.org/bot{token}/getMe")
        resp = urllib.request.urlopen(req, timeout=5)
        return '"ok":true' in resp.read().decode()
    except: return False

def check_memory():
    try:
        with open(MEMORY_FILE) as f: c = f.read()
        checks = [k in c for k in ["信息搜索规范", "任务追踪规范", "用户教育原则", "经验教训"]]
        return all(checks), f"{sum(checks)}/{len(checks)}项已记录"
    except FileNotFoundError:
        return False, "记忆文件不存在"

def main():
    h = datetime.now().hour
    tag = "morning" if h < 12 else ("afternoon" if h < 18 else "night")
    log(f"=== {tag} 自省 ===")
    
    ok_u, v_u = check_undici()
    ok_p = check_proxy()
    ok_t = check_telegram()
    ok_m, det_m = check_memory()
    
    log(f"  undici: {'✅' if ok_u else '❌'} v{v_u}")
    log(f"  proxy: {'✅' if ok_p else '❌'}")
    log(f"  telegram: {'✅' if ok_t else '❌'}")
    log(f"  memory: {'✅' if ok_m else '❌'} {det_m}")
    
    total = sum([ok_u, ok_p, ok_t, ok_m])
    log(f"  ── {total}/4 通过 ──")
    
    os.makedirs(MEMORY_DIR, exist_ok=True)
    with open(MEMORY_FILE, "a") as f:
        f.write(f"\n## 自省 {tag} {datetime.now().strftime('%H:%M')}\n")
        f.write(f"- undici: {'OK' if ok_u else 'NOK v'+str(v_u)}\n")
        f.write(f"- proxy: {'OK' if ok_p else 'NOK'}\n")
        f.write(f"- tg: {'OK' if ok_t else 'NOK'}\n")
        f.write(f"- mem: {'OK' if ok_m else 'NOK'}\n")
        f.write(f"- 通过: {total}/4\n")

if __name__ == "__main__":
    main()
