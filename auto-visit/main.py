import time
import random
import requests

def load_sites():
    with open("sites.txt", "r", encoding="utf-8") as f:
        return [line.strip() for line in f if line.strip()]

def visit(url):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
    }
    try:
        resp = requests.get(url, headers=headers, timeout=20)
        print(f"[OK] {url} 状态码: {resp.status_code}")
    except Exception as e:
        print(f"[ERROR] 访问 {url} 失败: {e}")

def main():
    sites = load_sites()
    print(f"[INFO] 共加载 {len(sites)} 个网站")

    for url in sites:
        # 每个网站访问前随机等待 10~120 分钟（600~7200 秒）
        delay = random.randint(600, 7200)
        print(f"\n[INFO] 即将访问：{url}")
        print(f"[INFO] 随机等待 {delay} 秒后开始访问")
        time.sleep(delay)

        visit(url)

if __name__ == "__main__":
    main()
    
