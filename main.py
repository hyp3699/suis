import time
import random
import requests
import urllib3
import os

# 关闭 SSL 警告
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# 读取网站列表 (保持原逻辑，读取同目录下的 sites.txt)
def load_sites():
    try:
        with open("sites.txt", "r", encoding="utf-8") as f:
            return [line.strip() for line in f if line.strip() and not line.startswith("#")]
    except FileNotFoundError:
        print("[ERROR] 找不到 sites.txt 文件")
        return []

# Telegram 推送函数
def send_telegram(bot_token, chat_id, message):
    if not bot_token or not chat_id:
        print("[WARN] Telegram 配置缺失，跳过推送")
        return
    
    url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
    try:
        # 使用 Markdown 格式让输出更整齐
        requests.post(url, data={"chat_id": chat_id, "text": message, "parse_mode": "Markdown"}, timeout=20)
    except Exception as e:
        print(f"[ERROR] Telegram 推送失败: {e}")

# 访问逻辑
def visit(url):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    }
    for attempt in range(1, 4):
        try:
            resp = requests.get(url, headers=headers, timeout=20, verify=False)
            return f"✅ `{url}` 状态码: {resp.status_code}"
        except Exception as e:
            if attempt < 3:
                time.sleep(2)
                continue
            return f"❌ `{url}` 访问失败: {str(e)[:50]}..."

def main():
    # 从环境变量获取敏感信息 (GitHub Actions 会自动填入)
    bot_token = os.environ.get("BOT_TOKEN")
    chat_id = os.environ.get("CHAT_ID")
    
    # 随机等待 5~30 秒 (模拟真人/防检测)
    extra_delay = random.randint(5, 30)
    print(f"[INFO] 随机等待 {extra_delay} 秒...")
    time.sleep(extra_delay)

    sites = load_sites()
    print(f"[INFO] 共加载 {len(sites)} 个网站")

    results = []
    for url in sites:
        res = visit(url)
        print(res)
        results.append(res)

    # 汇总发送，避免被 Telegram 频率限制
    if results:
        full_report = "🌐 **站点访问报告**\n\n" + "\n".join(results)
        send_telegram(bot_token, chat_id, full_report)

if __name__ == "__main__":
    main()
