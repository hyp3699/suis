import time
import random
import requests
import base64
import urllib3

# 关闭 SSL 警告
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# 固定时间触发后，再随机等待 5~30 秒
extra_delay = random.randint(5, 30)
print(f"[INFO] 固定时间触发，随机等待 {extra_delay} 秒")
time.sleep(extra_delay)

# 读取网站列表
def load_sites():
    with open("sites.txt", "r", encoding="utf-8") as f:
        return [line.strip() for line in f if line.strip() and not line.startswith("#")]

# 读取配置（混淆后的 Token + 推送开关）
def load_config():
    config = {}
    with open("config.txt", "r", encoding="utf-8") as f:
        for line in f:
            if "=" in line:
                key, value = line.strip().split("=", 1)
                config[key] = value
    return config

# Base64 解码
def decode(s):
    return base64.b64decode(s).decode()

# Telegram 推送
def send_telegram(bot_token, chat_id, message):
    url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
    try:
        requests.post(url, data={"chat_id": chat_id, "text": message})
    except Exception as e:
        print(f"[ERROR] Telegram 推送失败: {e}")

# 自动 SSL 容错 + 自动重试访问
def visit(url):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
    }

    for attempt in range(1, 4):  # 自动重试 3 次
        try:
            resp = requests.get(url, headers=headers, timeout=20, verify=False)
            return f"[OK] {url} 状态码: {resp.status_code}"

        except requests.exceptions.SSLError as e:
            return f"[SSL ERROR] {url} 证书验证失败: {e}"

        except Exception as e:
            if attempt < 3:
                time.sleep(2)  # 重试前等待 2 秒
                continue
            return f"[ERROR] {url} 访问失败（已重试 3 次）: {e}"

def main():
    sites = load_sites()
    config = load_config()

    # 解混淆（你在混淆网站生成的 Base64 分段）
    bot_token = decode(config["BOT_TOKEN_PART1"]) + decode(config["BOT_TOKEN_PART2"])
    chat_id = decode(config["CHAT_ID_BASE64"])

    # 推送开关
    push_enabled = config.get("TELEGRAM_PUSH", "on").lower() == "on"
    print(f"[INFO] Telegram 推送状态: {'开启' if push_enabled else '关闭'}")

    print(f"[INFO] 共加载 {len(sites)} 个网站")

    for url in sites:
        result = visit(url)
        print(result)

        # 如果开启推送，则发送 Telegram
        if push_enabled:
            send_telegram(bot_token, chat_id, result)

if __name__ == "__main__":
    main()
    
