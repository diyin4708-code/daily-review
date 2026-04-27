---
name: 吾日三省吾身
description: |
  每日三省吾身 — 早10点、午4点、晚10点定时自检OpenClaw核心状态（网络/代理/TG连接/记忆一致性），
  发现问题自动修复，并将结果写入记忆文件。受中国传统文化启发设计的AI自省技能。
  Daily self-check skill for OpenClaw agents. Auto-check undici, proxy, TG connection, and memory integrity
  at 10AM/4PM/10PM. Fix issues and log to memory files.
license: MIT
metadata:
  author: "@lingmunaixue"
  version: "1.0.0"
  keywords: [self-check, monitoring, health, memory, proxy, telegram, undici, 自省, 三省吾身]
  agent:
    requires:
      bins: ["python3"]
    install:
      - id: script
        kind: copy
        label: "安装每日三省到workspace"
user-invocable: true
---

# 吾日三省吾身

> 曾子曰：「吾日三省吾身——为人谋而不忠乎？与朋友交而不信乎？传不习乎？」
> AI 亦然。每天三次，自检自修。

## 功能

| 检查项 | 说明 | 自动修复 |
|--------|------|----------|
| 🔧 undici | 确保 ProxyAgent 可用（修复 undici 8.x bug） | ✅ 降级到 7.25 |
| 🌐 代理 | Clash/代理是否存活 | ❌ |
| 💬 TG | Telegram Bot 是否在线 | ❌ |
| 📝 记忆 | 规范是否已写入今日记忆文件 | ❌ |
| 📊 通过率 | 汇总并记录 | ✅ |

## 三个时间点

| 时辰 | 时间 | 意义 |
|------|------|------|
| 🌅 晨省 | 10:00 | 检查昨夜状态，开启新一天 |
| ☀️ 午省 | 16:00 | 检查日间运行情况 |
| 🌙 暮省 | 22:00 | 总结一天，确保睡后状态 |

## 安装

```bash
# 克隆仓库
git clone https://github.com/diyin4708-code/吾日三省吾身.git ~/.openclaw/workspace/skills/daily-review

# 添加定时任务
(crontab -l 2>/dev/null; echo "0 10 * * * python3 ~/.openclaw/workspace/skills/daily-review/check.py morning"; echo "0 16 * * * python3 ~/.openclaw/workspace/skills/daily-review/check.py afternoon"; echo "0 22 * * * python3 ~/.openclaw/workspace/skills/daily-review/check.py night") | crontab -
```

## 运行效果

```
[10:00:00] === 晨省 ===
[10:00:01]   undici: ✅ v7.25.0
[10:00:03]   proxy: ✅
[10:00:05]   telegram: ✅
[10:00:05]   memory: ✅ 4/4 项已记录
[10:00:05]   ── 4/4 通过 ──
```

## 自定义

修改 `check.py` 中的检查项和修复逻辑，添加适合你自己的检查规则。

## 灵感

《论语·学而》：「吾日三省吾身——为人谋而不忠乎？与朋友交而不信乎？传不习乎？」

两千年前的智慧放在 AI 时代依然适用：
- 为人谋 → AI 对用户是否尽心？
- 与朋友交 → 多Agent协作是否守信？
- 传不习 → 学到的教训是否践行？

每天三次，不过几行代码的事。但写下来、跑起来、改到位——这就是「省」的意义。

Made with ❤️ by [@lingmunaixue](https://x.com/lingmunaixue)
