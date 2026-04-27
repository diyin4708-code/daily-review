---
name: daily-review
description: |
  每日三省吾身 — 早10点、午4点、晚10点定时自检OpenClaw核心状态（网络/代理/TG连接/记忆一致性），
  发现问题自动修复，并将结果写入记忆文件。受中国传统文化启发设计的AI自省技能。
  Daily self-check skill for OpenClaw agents. Auto-check undici, proxy, TG connection, and memory integrity
  at 10AM/4PM/10PM. Fix issues and log to memory files.
license: MIT
metadata:
  author: lingmunaixue
  version: "1.0.0"
  keywords: [self-check, monitoring, health, memory, proxy, telegram, undici]
  agent:
    requires:
      bins: ["python3"]
    install:
      - id: script
        kind: copy
        label: "Install daily-review to workspace"
user-invocable: true
---

# 每日三省吾身 | Daily Review

10:00 / 16:00 / 22:00 三个时间点自动检查 OpenClaw 核心状态，发现问题自动修复并记录到记忆文件。

> 学而不思则罔，思而不学则殆。AI 亦然。

## 功能

- ⏰ 三个时间点自动触发（cron 定时）
- 🔍 检查 undici 版本（降级修复 8.x ProxyAgent bug）
- 🌐 检查代理连通性（Clash/其他）
- 💬 检查 Telegram Bot 连接状态
- 📝 检查记忆文件是否包含必要规范
- 🔧 发现问题自动修复（undici 替换等）
- 📊 通过率汇总写入记忆

## 安装

```bash
# 复制技能到 workspace
cp -r daily-review/ ~/.openclaw/workspace/skills/

# 添加 cron 任务
(crontab -l 2>/dev/null; echo "0 10 * * * python3 ~/.openclaw/workspace/skills/daily-review/check.py morning"; echo "0 16 * * * python3 ~/.openclaw/workspace/skills/daily-review/check.py afternoon"; echo "0 22 * * * python3 ~/.openclaw/workspace/skills/daily-review/check.py night") | crontab -
```

## 检查项目

| 项目 | 说明 | 自动修复 |
|------|------|----------|
| undici 版本 | 确保 ProxyAgent 可用 | ✅ 降级到 7.25 |
| 代理连接 | Clash 代理是否存活 | ❌ |
| TG 连接 | Bot 是否在线 | ❌ |
| 记忆完整性 | 规范是否已写入 | ❌ |

## 输出示例

```
[10:00:00] === morning 自省开始 ===
[10:00:01]   undici: ✅ v7.25.0
[10:00:03]   proxy: ✅
[10:00:05]   telegram: ✅
[10:00:05]   memory: ✅ 4/4 项已记录
[10:00:05]   ── 4/4 通过 ──
```

## 自定义

修改 `check.py` 中的检查项和修复逻辑，添加适合你自己的检查规则。

## Credits

灵感来自《论语·学而》：「吾日三省吾身——为人谋而不忠乎？与朋友交而不信乎？传不习乎？」

Made with ❤️ by @lingmunaixue
