#!/usr/bin/env python3
import json
import os
import shutil
import datetime
import subprocess

# --- 色彩與標籤 ---
GREEN = "\033[92m"
BLUE = "\033[94m"
YELLOW = "\033[93m"
RED = "\033[91m"
RESET = "\033[0m"

# --- 設定 ---
WORKS_JSON = "data/works.json"
ASSETS_DIR = "assets"
OPTIMIZE_SCRIPT = "scripts/optimize.py"

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def print_header():
    print(f"{BLUE}========================================")
    print("   AI 電商行銷設計師 Ultra 管理助手")
    print(f"========================================{RESET}\n")

def get_input(prompt, default=None):
    if default:
        val = input(f"{prompt} [{default}]: ").strip()
        return val if val else default
    return input(f"{prompt}: ").strip()

def add_new_work():
    clear_screen()
    print_header()
    print(f"{YELLOW}--- 新增作品 ---{RESET}")

    # 1. 圖片來源路徑
    while True:
        img_path = get_input("請輸入圖片路徑 (可直接將檔案拖進來或輸入路徑)")
        # 處理 Mac/Linux 可能帶有的轉義空白
        img_path = img_path.replace("\\ ", " ").strip("'").strip('"')
        if os.path.exists(img_path):
            break
        print(f"{RED}錯誤：找不到檔案，請再試一次。{RESET}")

    # 2. 自動產生 ID 與檔名
    now = datetime.datetime.now()
    timestamp = now.strftime("%Y%m%d_%H%M%S")
    extension = os.path.splitext(img_path)[1].lower()
    if not extension: extension = ".png"
    
    new_filename = f"work_{timestamp}{extension}"
    dest_path = os.path.join(ASSETS_DIR, new_filename)

    # 3. 填寫資訊
    title = get_input("作品標題")
    
    print("\n選擇分類：")
    print("1. 廣告素材 (ad-creatives)")
    print("2. 行銷視覺 (marketing-visuals)")
    print("3. 網頁設計 (landing-pages)")
    print("4. 品牌概念 (branding)")
    print("5. 社群行銷 (social-media)")
    cat_idx = get_input("請輸入編號", "1")
    
    cat_map = {
        "1": "ad-creatives",
        "2": "marketing-visuals",
        "3": "landing-pages",
        "4": "branding",
        "5": "social-media"
    }
    category = cat_map.get(cat_idx, "ad-creatives")
    
    date = get_input("日期 (YYYY-MM-DD)", now.strftime("%Y-%m-%d"))

    # 4. 搬移檔案
    print(f"\n{BLUE}正在搬移與重命名檔案...{RESET}")
    shutil.copy(img_path, dest_path)

    # 5. 更新 JSON
    print(f"{BLUE}正在更新資料庫...{RESET}")
    try:
        with open(WORKS_JSON, 'r', encoding='utf-8') as f:
            works = json.load(f)
    except Exception:
        works = []

    # 隨機產生 ID 或遞增
    new_id = str(len(works) + 1)
    
    new_entry = {
        "id": new_id,
        "title": title,
        "image": f"assets/{new_filename}",
        "category": category,
        "date": date
    }
    works.append(new_entry)

    with open(WORKS_JSON, 'w', encoding='utf-8') as f:
        json.dump(works, f, indent=2, ensure_ascii=False)

    # 6. 觸發優化
    print(f"{BLUE}觸發圖片優化腳本...{RESET}")
    subprocess.run(["python3", OPTIMIZE_SCRIPT], stdout=subprocess.DEVNULL)

    print(f"\n{GREEN}🎉 作品新增成功！{RESET}")
    print(f"檔案位置：{dest_path}")
    print(f"作品標題：{title}")

    # 7. Git 推送詢問
    if get_input("是否立即發佈到 GitHub? (y/n)", "y").lower() == 'y':
        print(f"{BLUE}同步中...{RESET}")
        subprocess.run(["git", "add", "."])
        subprocess.run(["git", "commit", "-m", f"feat: add new work '{title}'"])
        subprocess.run(["git", "push"])
        print(f"{GREEN}✅ 已同步至 GitHub。{RESET}")

def main():
    while True:
        clear_screen()
        print_header()
        print("1. 新增作品")
        print("2. 執行圖片優化 (全部)")
        print("3. 結束")
        
        choice = get_input("\n請選擇功能 (1-3)", "1")
        
        if choice == "1":
            add_new_work()
            input("\n按任意鍵回到選單...")
        elif choice == "2":
            subprocess.run(["python3", OPTIMIZE_SCRIPT])
            input("\n按任意鍵回到選單...")
        elif choice == "3":
            print("再見！")
            break

if __name__ == "__main__":
    main()
