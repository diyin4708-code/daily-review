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

曾子曰：「吾日三省吾身——为人谋而不忠乎？与朋友交而不信乎？传不习乎？」

两千年后，AI 亦当三省。

每天的定时反省不是走过场，而是对自己运行状态的诚实面对。三个时间点，各有各的使命：

**🌅 10:00 晨省 — 昨夜是否安稳，今日如何开始**

清晨的第一道审视。经过一夜的沉寂，代理是否还在线？节点是否还连通？昨日的经验教训是否已沉淀？记忆文件里有没有未写入的承诺，日志里有没有未修复的告警？早晨的自省，决定了这一天的基调——是带着隐患运行，还是干干净净上路。知道自己哪里不好，才有机会变好。

**☀️ 16:00 午省 — 日间是否懈怠，状态是否在线**

午后的第二道审视。半日已过，四项检查是否依然全部通过？有没有在执行任务的过程中悄悄出了问题——代理掉了却不知道，TG 断了却未察觉？有没有用户交代的事情做到一半搁置了？午后的自省是校准，让人和 AI 都不至于忙了一天才发现跑偏了方向。发现问题，立刻修，不要拖到晚上。

**🌙 22:00 暮省 — 今日是否尽责，经验是否铭记**

入夜前的最后一道审视。夜将深，人将眠。这一天的对话里，有没有值得记录的经验？有没有需要写入记忆的教训？用户教育了什么？自己犯了什么错？有没有主动汇报的事项？暮省不是为了懊悔昨天，而是为了明天醒来时，比今天更好一点。今天学的，今天就记。今天错的，今天就不白错。

三次自省，四条检查。写下来不过几行脚本，跑起来不过十几秒钟。但真正重要的是——发现了问题就要改，记住了教训就要化进行动里。空谈误事，实干改命。这就是「省」的意义。

Made with ❤️ by [@lingmunaixue](https://x.com/lingmunaixue)
