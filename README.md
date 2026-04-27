# 🦞 每日三省吾身 | Daily Review

OpenClaw 定时自检技能。每天 10:00 / 16:00 / 22:00 自动检查核心状态并修复问题。

## 快速开始

```bash
cd ~/.openclaw/workspace/skills/
git clone https://github.com/diyin4708-code/daily-review.git

# 添加 cron
(crontab -l 2>/dev/null; echo "0 10 * * * python3 ~/.openclaw/workspace/skills/daily-review/check.py morning"; echo "0 16 * * * python3 ~/.openclaw/workspace/skills/daily-review/check.py afternoon"; echo "0 22 * * * python3 ~/.openclaw/workspace/skills/daily-review/check.py night") | crontab -
```

## 灵感

《论语·学而》：吾日三省吾身

Made with ❤️ by [@lingmunaixue](https://x.com/lingmunaixue)
