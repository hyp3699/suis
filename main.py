import os
import time
import random
import requests
import urllib3

# 关闭 SSL 警告
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def load_config():
    """从 config.txt 读取配置信息"""
    config = {}
    if os.path.exists("config.txt"):
        with open("config.txt", "r", encoding="utf-8") as f:
            for line in f:
                if "=" in line and not line.startswith("#"):
                    key, value = line.strip().split("=", 1)
                    config[key.strip()] = value.strip()
    return config

def load_sites():
    """读取网站列表 sites.txt"""
    if os.path.exists("sites.txt"):
        with open("sites.txt", "r", encoding="utf-8") as f:
            return [line.strip() for line in f if line.strip() and not line.startswith("#")]
    return []

def send_telegram(bot_token, chat_id, message):
    """发送 Telegram 消息"""
    url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
    try:
        requests.post(url, data={"chat_id": chat_id, "text": message, "parse_mode": "Markdown"}, timeout=20)
    except Exception as e:
        print(f"[ERROR] Telegram 推送失败: {e}")

def visit(url):
    """访问网站"""
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"}
    try:
        resp = requests.get(url, headers=headers, timeout=20, verify=False)
        return f"✅ `{url}` 状态: {resp.status_code}"
    except:
        return f"❌ `{url}` 访问失败"

def main():
    # 加载本地配置
    config = load_config()
    
    # 优先从环境变量获取 Token（为了安全），从 config.txt 获取开关（为了方便）
    bot_token = os.environ.get("BOT_TOKEN")
    chat_id = os.environ.get("CHAT_ID")
    
    # 读取开关：默认为 on，除非你在 config.txt 里写了 TELEGRAM_PUSH=off
    push_switch = config.get("TELEGRAM_PUSH", "on").lower()
    push_enabled = (push_switch == "on")

    sites = load_sites()
    if not sites:
        print("[ERROR] 未找到待访问站点")
        return

    # 随机等待
    time.sleep(random.randint(5, 20))

    print(f"[INFO] 开始访问，推送开关状态: {push_switch}")
    results = []
    for url in sites:
        res = visit(url)
        print(res)
        results.append(res)

    # 执行推送逻辑
    if push_enabled:
        if bot_token and chat_id:
            report = "🌐 **站点监控报告**\n\n" + "\n".join(results)
            send_telegram(bot_token, chat_id, report)
        else:
            print("[WARN] 推送已开启，但 GitHub Secrets 未配置 BOT_TOKEN 或 CHAT_ID")
    else:
        print("[INFO] 推送已关闭 (config.txt 设置为 off)")

if __name__ == "__main__":
    main()
