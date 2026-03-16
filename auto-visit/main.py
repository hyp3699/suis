import time
import random
import requests

def load_url():
    with open("config.txt", "r", encoding="utf-8") as f:
        return f.read().strip()

def main():
    # 随机等待 10~120 分钟（600~7200 秒）
    delay = random.randint(600, 7200)
    print(f"[INFO] 随机等待 {delay} 秒后开始访问网站")
    time.sleep(delay)

    # 从 config.txt 读取网站
    url = load_url()
    print(f"[INFO] 开始访问：{url}")

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
    }

    try:
        resp = requests.get(url, headers=headers, timeout=20)
        print(f"[INFO] 状态码：{resp.status_code}")
        print("[INFO] 返回内容：")
        print(resp.text[:500])
    except Exception as e:
        print(f"[ERROR] 请求失败：{e}")

if __name__ == "__main__":
    main()
    
