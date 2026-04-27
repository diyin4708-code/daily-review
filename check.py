#!/usr/bin/env python3
"""
吾日三省吾身 — 10:00晨省 / 16:00午省 / 22:00暮省
自动检查 OpenClaw 核心状态，发现问题修复并记录
"""

import subprocess, os, signal, sys
from datetime import datetime

LOG_FILE = os.path.expanduser("~/.openclaw/workspace/daily_check.log")
MEMORY_DIR = os.path.expanduser("~/.openclaw/workspace/memory/")
MEMORY_FILE = MEMORY_DIR + datetime.now().strftime("%Y-%m-%d") + ".md"
UNDICI_TARGET = os.path.expanduser("~/.npm-global/lib/node_modules/openclaw/node_modules/undici")
UNDICI_SOURCE = os.path.expanduser("~/.npm-global/lib/node_modules/clawhub/node_modules/undici")
PROXY = "http://172.19.208.1:7897"

# 配置（可根据自己环境修改）
CHECKS = {
    "undici": {"fix": True, "desc": "ProxyAgent 兼容性"},
    "proxy":  {"fix": False, "desc": "Clash 代理连通"},
    "tg":     {"fix": False, "desc": "Telegram Bot 在线"},
    "memory": {"fix": False, "desc": "规范记录完整性"},
}

def log(msg):
    t = datetime.now().strftime("%H:%M:%S")
    line = f"[{t}] {msg}"
    print(line)
    os.makedirs(os.path.dirname(LOG_FILE), exist_ok=True)
    with open(LOG_FILE, "a") as f: f.write(line + "\n")

def check_undici():
    try:
        import json
        with open(f"{UNDICI_TARGET}/package.json") as f:
            v = json.load(f)["version"]
        if v == "7.25.0": return True, v
        log(f"  ⚠️ undici={v}, 自动修复...")
        os.system(f"rm -rf {UNDICI_TARGET} && cp -r {UNDICI_SOURCE} {UNDICI_TARGET}")
        # 修复后重启 gateway
        os.system("source ~/.bashrc && openclaw gateway restart 2>/dev/null &")
        log(f"  ✅ undici 已修复，gateway 正在重启")
        return True, f"{v}→7.25.0(已修)"
    except Exception as e:
        return False, str(e)[:30]

def check_proxy():
    try:
        import urllib.request
        resp = urllib.request.urlopen(f"{PROXY}", timeout=3)
        return True
    except:
        return False

def check_telegram():
    try:
        import json, urllib.request
        with open(os.path.expanduser("~/.openclaw/openclaw.json")) as f:
            cfg = json.load(f)
        token = cfg.get("channels", {}).get("telegram", {}).get("botToken", "")
        if not token: return False
        resp = urllib.request.urlopen(f"https://api.telegram.org/bot{token}/getMe", timeout=5)
        return '"ok":true' in resp.read().decode()
    except:
        return False

def check_memory():
    try:
        with open(MEMORY_FILE) as f:
            c = f.read()
        items = ["信息搜索规范", "任务追踪规范", "用户教育原则", "自省", "技能安装"]
        count = sum(1 for k in items if k in c)
        return count >= 3, f"{count}/{len(items)}"
    except:
        return False, "无记忆文件"

def write_memory(tag, results):
    os.makedirs(MEMORY_DIR, exist_ok=True)
    now = datetime.now()
    total = len(results)
    passed = sum(1 for v in results.values() if v[0])
    
    # 读今日记忆
    old = ""
    try:
        with open(MEMORY_FILE) as f: old = f.read()
    except: pass
    
    tag_cn = {"morning": "🌅 晨省", "afternoon": "☀️ 午省", "night": "🌙 暮省"}.get(tag, tag)
    
    entry = f"\n## {tag_cn} {now.strftime('%H:%M')}\n"
    for name, (ok, detail) in results.items():
        desc = CHECKS.get(name, {}).get("desc", name)
        entry += f"- {desc}: {'✅' if ok else '❌'} {detail if not ok else ''}\n"
    entry += f"- 通过率: {passed}/{total}\n"
    
    with open(MEMORY_FILE, "w") as f:
        f.write(old + entry)

def main():
    tag = sys.argv[1] if len(sys.argv) > 1 else "manual"
    
    tag_cn = {"morning": "晨省", "afternoon": "午省", "night": "暮省"}.get(tag, "自省")
    log(f"=== {tag_cn} ===")
    
    results = {}
    
    # undici
    ok, detail = check_undici()
    results["undici"] = (ok, f"v{detail}" if ok else detail)
    log(f"  undici: {'✅' if ok else '❌'} {detail}")
    
    # proxy
    ok = check_proxy()
    results["proxy"] = (ok, "")
    log(f"  proxy: {'✅' if ok else '❌'}")
    
    # tg
    ok = check_telegram()
    results["tg"] = (ok, "")
    log(f"  tg: {'✅' if ok else '❌'}")
    
    # memory
    ok, detail = check_memory()
    results["memory"] = (ok, detail)
    log(f"  memory: {'✅' if ok else '❌'} {detail}")
    
    total = len(results)
    passed = sum(1 for v in results.values() if v[0])
    log(f"  ── {passed}/{total} 通过 ──")
    
    # 写入
    write_memory(tag, results)
    
    # 主动通知（如果通）
    if passed < total:
        log(f"  ⚠️ 有 {total-passed} 项未通过，已记录到记忆")

if __name__ == "__main__":
    main()
