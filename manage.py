#!/usr/bin/env python3
import json
import os
import shutil
import datetime
import subprocess
import shlex
import glob

# --- 色彩與標籤 ---
GREEN = "\033[92m"
BLUE = "\033[94m"
YELLOW = "\033[93m"
RED = "\033[91m"
RESET = "\033[0m"

# --- 設定 ---
WORKS_JSON = "data/works.json"
ASSETS_DIR = "assets"
IMPORT_DIR = "import_queue"
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

def pick_category():
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
    return cat_map.get(cat_idx, "ad-creatives")

def add_works_to_json(entries):
    try:
        with open(WORKS_JSON, 'r', encoding='utf-8') as f:
            works = json.load(f)
    except Exception:
        works = []
    
    # 計算起始 ID
    start_id = 1
    if works:
        try:
            ids = [int(w['id']) for w in works if w['id'].isdigit()]
            if ids: start_id = max(ids) + 1
        except:
            start_id = len(works) + 1

    for i, entry in enumerate(entries):
        entry['id'] = str(start_id + i)
        works.append(entry)

    with open(WORKS_JSON, 'w', encoding='utf-8') as f:
        json.dump(works, f, indent=2, ensure_ascii=False)

def process_batch(paths, category, date, commit_msg_prefix="batch add"):
    new_entries = []
    print(f"\n{BLUE}正在處理檔案...{RESET}")
    
    for i, path in enumerate(paths):
        now = datetime.datetime.now()
        timestamp = now.strftime("%Y%m%d_%H%M%S")
        extension = os.path.splitext(path)[1].lower()
        if not extension: extension = ".png"
        
        # 避免同秒產生的衝突，加上序號
        new_filename = f"work_{timestamp}_{i:03d}{extension}"
        dest_path = os.path.join(ASSETS_DIR, new_filename)
        
        # 搬移 (如果是從 import_queue 則是搬移，如果是拖入則是複製)
        if path.startswith(IMPORT_DIR):
            shutil.move(path, dest_path)
        else:
            shutil.copy(path, dest_path)
        
        # 標題預設為原檔名
        original_name = os.path.splitext(os.path.basename(path))[0]
        
        new_entries.append({
            "title": original_name,
            "image": f"assets/{new_filename}",
            "category": category,
            "date": date
        })
        print(f"  [{i+1}/{len(paths)}] 已處理: {original_name}")

    # 寫入 JSON
    print(f"{BLUE}更新資料庫...{RESET}")
    add_works_to_json(new_entries)

    # 執行優化
    print(f"{BLUE}批次優化圖片中...{RESET}")
    subprocess.run(["python3", OPTIMIZE_SCRIPT], stdout=subprocess.DEVNULL)

    print(f"\n{GREEN}🎉 處理完成！共新增 {len(paths)} 件作品。{RESET}")

    # Git 同步
    if get_input("是否立即將更新發佈到 GitHub? (y/n)", "y").lower() == 'y':
        print(f"{BLUE}同步中...{RESET}")
        subprocess.run(["git", "add", "."])
        subprocess.run(["git", "commit", "-m", f"feat: {commit_msg_prefix} {len(paths)} works"])
        subprocess.run(["git", "push"])
        print(f"{GREEN}✅ 已全部同步至 GitHub。{RESET}")

def folder_import():
    clear_screen()
    print_header()
    print(f"{YELLOW}--- 資料夾全速導入 ---{RESET}")
    print(f"請將所有圖片放入專案目錄下的 '{IMPORT_DIR}/' 資料夾中。")
    
    # 支援的副檔名
    extensions = ['*.jpg', '*.jpeg', '*.png', '*.webp', '*.JPG', '*.JPEG', '*.PNG', '*.WEBP']
    files_to_import = []
    for ext in extensions:
        files_to_import.extend(glob.glob(os.path.join(IMPORT_DIR, ext)))
    
    # 排除 .gitkeep
    files_to_import = [f for f in files_to_import if os.path.basename(f) != '.gitkeep']

    if not files_to_import:
        print(f"\n{RED}掃描結果：'{IMPORT_DIR}/' 資料夾目前是空的。{RESET}")
        print("請放入圖片後再執行此功能。")
        return

    print(f"\n{GREEN}掃描到 {len(files_to_import)} 張待匯入的圖片。{RESET}")
    
    category = pick_category()
    date = get_input("匯入作品的日期 (YYYY-MM-DD)", datetime.datetime.now().strftime("%Y-%m-%d"))

    if get_input(f"即將開始匯入這 {len(files_to_import)} 筆資料，確定嗎？ (y/n)", "y").lower() != 'y':
        return

    process_batch(files_to_import, category, date, commit_msg_prefix="folder import")

def batch_add_works():
    clear_screen()
    print_header()
    print(f"{YELLOW}--- 批量新增作品 (拖入方式) ---{RESET}")
    
    raw_input = get_input("請拖入多個圖片檔案")
    if not raw_input: return

    try:
        if "\\" in raw_input and " '" not in raw_input:
             img_paths = [p.strip() for p in raw_input.split(" /") if p.strip()]
             if not img_paths[0].startswith("/"): img_paths[0] = "/" + img_paths[0]
             img_paths = [img_paths[0]] + ["/" + p for p in img_paths[1:]]
        else:
            img_paths = shlex.split(raw_input)
    except Exception as e:
        print(f"{RED}路徑解析失敗：{e}{RESET}")
        return

    valid_paths = [p for p in img_paths if os.path.exists(p)]
    if not valid_paths:
        print(f"{RED}錯誤：找不到有效的檔案。{RESET}")
        return

    print(f"\n{GREEN}已偵測到 {len(valid_paths)} 個有效檔案。{RESET}")
    
    category = pick_category()
    date = get_input("日期 (YYYY-MM-DD)", datetime.datetime.now().strftime("%Y-%m-%d"))

    process_batch(valid_paths, category, date, commit_msg_prefix="drag batch")

def single_add_work():
    clear_screen()
    print_header()
    print(f"{YELLOW}--- 單件新增作品 ---{RESET}")

    img_path = get_input("請輸入圖片路徑")
    img_path = img_path.replace("\\ ", " ").strip("'").strip('"')
    if not os.path.exists(img_path):
        print(f"{RED}錯誤：檔案不存在。{RESET}")
        return

    category = pick_category()
    title = get_input("作品標題")
    date = get_input("日期 (YYYY-MM-DD)", datetime.datetime.now().strftime("%Y-%m-%d"))

    now = datetime.datetime.now()
    new_filename = f"work_{now.strftime('%Y%m%d_%H%M%S')}{os.path.splitext(img_path)[1].lower()}"
    dest_path = os.path.join(ASSETS_DIR, new_filename)
    shutil.copy(img_path, dest_path)
    
    add_works_to_json([{
        "title": title,
        "image": f"assets/{new_filename}",
        "category": category,
        "date": date
    }])

    print(f"{BLUE}優化中...{RESET}")
    subprocess.run(["python3", OPTIMIZE_SCRIPT], stdout=subprocess.DEVNULL)
    print(f"{GREEN}🎉 新增完成！{RESET}")
    
    if get_input("同步 GitHub? (y/n)", "y").lower() == 'y':
        subprocess.run(["git", "add", "."])
        subprocess.run(["git", "commit", "-m", f"feat: add work '{title}'"])
        subprocess.run(["git", "push"])

def main():
    while True:
        clear_screen()
        print_header()
        print(f"{GREEN}★ 核心功能：{RESET}")
        print(f" {YELLOW}1. 批量資料夾導入 (將圖片放入 {IMPORT_DIR}/ 後執行){RESET}")
        print(" 2. 批量拖拉導入 (一次拖入多個檔案)")
        print(" 3. 單件手動新增")
        print(f"\n{GREEN}★ 工具功能：{RESET}")
        print(" 4. 執行圖片優化 (目前所有資產)")
        print(" 5. 結束")
        
        choice = get_input("\n請選擇功能 (1-5)", "1")
        
        if choice == "1":
            folder_import()
            input("\n按任意鍵繼續...")
        elif choice == "2":
            batch_add_works()
            input("\n按任意鍵繼續...")
        elif choice == "3":
            single_add_work()
            input("\n按任意鍵繼續...")
        elif choice == "4":
            subprocess.run(["python3", OPTIMIZE_SCRIPT])
            input("\n按任意鍵繼續...")
        elif choice == "5":
            print("再見！")
            break

if __name__ == "__main__":
    if not os.path.exists(IMPORT_DIR):
        os.makedirs(IMPORT_DIR)
    main()
