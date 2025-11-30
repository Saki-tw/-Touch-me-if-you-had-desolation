import requests
from bs4 import BeautifulSoup
import time
import random
import sys

# ================= ⚙️ 匿蹤雷達設定 =================
BOARDS = ["Soft_Job", "Tech_Job", "CodeJob", "Wanted"]
KEYWORDS = ["RAG", "LLM", "Python", "Remote", "遠端", "兼職", "接案"]

# 基礎冷卻時間 (秒)
BASE_SLEEP = 300 
# 隨機抖動範圍 (秒) -> 會在 BASE_SLEEP 基礎上加減
JITTER_RANGE = (-50, 120) 

# 偽裝身分池
USER_AGENTS = [
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.2 Safari/605.1.15",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36"
]
# ===================================================

def get_random_header():
    return {
        "User-Agent": random.choice(USER_AGENTS),
        "Cookie": "over18=1" # PTT 成人驗證 Cookie
    }

def scan_board(board):
    url = f"https://www.ptt.cc/bbs/{board}/index.html"
    try:
        # 使用隨機 Header
        resp = requests.get(url, headers=get_random_header(), timeout=15)
        
        if resp.status_code == 200:
            soup = BeautifulSoup(resp.text, "html.parser")
            posts = soup.find_all("div", class_="r-ent")
            
            print(f"   ✅ {board}: 訊號接收正常")
            
            # 簡單解析邏輯 (這裡只示範掃描，不包含通知邏輯，妳原本的通知邏輯可加回來)
            # for post in posts:
            #    title = post.find("div", class_="title").text.strip()
            #    ...
            return True
        else:
            print(f"   ⚠️ {board}: HTTP {resp.status_code}")
            return False

    except Exception as e:
        print(f"   ❌ {board} 掃描失敗: {e}")
        return False

def main():
    print("🛰️ SakiRadar V2 (Stealth Mode) 啟動...")
    print("   ↳ 載入隨機偽裝與時間抖動模組")

    consecutive_fails = 0

    while True:
        print(f"\n[{time.strftime('%H:%M:%S')}] 開始掃描迴圈...")
        
        any_success = False
        for board in BOARDS:
            if scan_board(board):
                any_success = True
            
            # 板塊之間的微小延遲 (模擬人類點擊)
            time.sleep(random.uniform(2, 5))

        # 判斷是否被封鎖
        if not any_success:
            consecutive_fails += 1
            print(f"🔥 警告：全域掃描失敗 ({consecutive_fails} 次)")
            if consecutive_fails >= 3:
                print("💀 偵測到持續封鎖。進入長眠模式 (30分鐘)...")
                time.sleep(1800)
                consecutive_fails = 0
                continue
        else:
            consecutive_fails = 0

        # 計算下一次掃描時間 (加入抖動)
        jitter = random.randint(JITTER_RANGE[0], JITTER_RANGE[1])
        next_sleep = BASE_SLEEP + jitter
        if next_sleep < 60: next_sleep = 60 # 至少睡 1 分鐘

        print(f"💤 進入變頻休眠: {next_sleep} 秒 (Jitter: {jitter})")
        time.sleep(next_sleep)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n👋 雷達關閉。")
        sys.exit(0)