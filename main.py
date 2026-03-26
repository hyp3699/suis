import os
import time
import random
import requests
import urllib3

# 禁用 SSL 警告
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def load_config():
    """只从 config.txt 读取推送开关状态"""
    config = {}
    if os.path.exists("config.txt"):
        with open("config.txt", "r", encoding="utf-8") as f:
            for line in f:
                if "=" in line and not line.startswith("#"):
                    key, value = line.strip().split("=", 1)
                    config[key.strip()] = value.strip()
    return config

def load_sites():
    """读取 sites.txt 里的网站列表"""
    if os.path.exists("sites.txt"):
        with open("sites.txt", "r", encoding="utf-8") as f:
            return [line.strip() for line in f if line.strip() and not line.startswith("#")]
    return []

def send_telegram(bot_token, chat_id, message):
    """发送汇总推送"""
    url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
    try:
        requests.post(url, data={"chat_id": chat_id, "text": message, "parse_mode": "Markdown"}, timeout=20)
    except Exception as e:
        print(f"[ERROR] 推送失败: {e}")

def visit(url):
    """访问单个网站"""
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"}
    try:
        resp = requests.get(url, headers=headers, timeout=20, verify=False)
        return f"✅ `{url}` 状态: {resp.status_code}"
    except:
        return f"❌ `{url}` 访问异常"

def main():
    # 1. 加载配置（Token 从环境变量取，开关从文件取）
    bot_token = os.environ.get("BOT_TOKEN")
    chat_id = os.environ.get("CHAT_ID")
    
    config = load_config()
    push_enabled = config.get("TELEGRAM_PUSH", "on").lower() == "on"
    
    sites = load_sites()
    if not sites:
        print("[ERROR] sites.txt 为空")
        return

    print(f"[INFO] 任务开始，推送开关: {'开启' if push_enabled else '关闭'}")
    results = []

    # 2. 循环访问网站
    for index, url in enumerate(sites):
        res = visit(url)
        print(res)
        results.append(res)
        
        # --- 重点：每个网站访问后停留 10 秒左右 ---
        if index < len(sites) - 1: # 最后一个网站访问完不需要等
            wait_time = random.randint(9, 12) # 10秒左右波动，更像真人
            print(f"[WAIT] 停留 {wait_time} 秒...")
            time.sleep(wait_time)

    # 3. 最终汇总推送
    if push_enabled and bot_token and chat_id:
        report = "🌐 **站点访问报告**\n\n" + "\n".join(results)
        send_telegram(bot_token, chat_id, report)
        print("[INFO] 推送任务完成")
    else:
        print("[INFO] 推送跳过（未配置环境或开关已关闭）")

if __name__ == "__main__":
    main()
