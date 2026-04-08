#!/usr/bin/env python3
import os
import subprocess
import json
import sys

# --- 色彩與標籤 ---
GREEN = "\033[92m"
BLUE = "\033[94m"
YELLOW = "\033[93m"
RESET = "\033[0m"

# --- 設定 ---
ASSETS_DIR = "assets"
WORKS_JSON = "data/works.json"
MAX_WIDTH = 1600
QUALITY = 80 # 0-100

def optimize_images():
    print(f"{BLUE}🚀 開始優化與轉換 assets 中的圖檔...{RESET}")
    
    if not os.path.exists(ASSETS_DIR):
        print(f"找不到 {ASSETS_DIR} 資料夾。")
        return

    # 1. 讀取資料庫 (為了同步副檔名變更)
    works = []
    if os.path.exists(WORKS_JSON):
        with open(WORKS_JSON, 'r', encoding='utf-8') as f:
            works = json.load(f)

    path_mapping = {}
    converted = 0
    optimized = 0

    for filename in os.listdir(ASSETS_DIR):
        if filename.startswith('.'): continue
        
        filepath = os.path.join(ASSETS_DIR, filename)
        ext = os.path.splitext(filename)[1].lower()
        
        if ext == '.png':
            # 自動將 PNG 轉為 JPG
            new_filename = os.path.splitext(filename)[0] + ".jpg"
            new_filepath = os.path.join(ASSETS_DIR, new_filename)
            
            try:
                subprocess.run([
                    "sips",
                    "-s", "format", "jpeg",
                    "--resampleWidth", str(MAX_WIDTH),
                    "-s", "formatOptions", str(QUALITY),
                    filepath,
                    "--out", new_filepath
                ], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
                
                os.remove(filepath)
                path_mapping[f"assets/{filename}"] = f"assets/{new_filename}"
                print(f"{YELLOW}🔄 轉換{RESET} {filename:30} -> {new_filename}")
                converted += 1
            except Exception as e:
                print(f"❌ 轉換 {filename} 失敗: {e}")
                
        elif ext in ['.jpg', '.jpeg', '.webp']:
            try:
                old_size = os.path.getsize(filepath) / 1024
                subprocess.run([
                    "sips",
                    "--resampleWidth", str(MAX_WIDTH),
                    "-s", "formatOptions", str(QUALITY),
                    filepath
                ], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
                new_size = os.path.getsize(filepath) / 1024
                reduction = ((old_size - new_size) / old_size) * 100 if old_size > 0 else 0
                
                print(f"{GREEN}✔{RESET} {filename:30} | {old_size:7.1f}KB -> {new_size:7.1f}KB ({reduction:5.1f}% 節省)")
                optimized += 1
            except Exception as e:
                print(f"❌ 優化 {filename} 失敗: {e}")

    # 2. 同步資料庫
    if path_mapping and works:
        print(f"\n{BLUE}📝 正在同步資料庫路徑...{RESET}")
        updated_count = 0
        for work in works:
            old_path = work.get("image")
            if old_path in path_mapping:
                work["image"] = path_mapping[old_path]
                updated_count += 1
        
        with open(WORKS_JSON, 'w', encoding='utf-8') as f:
            json.dump(works, f, ensure_ascii=False, indent=2)
        print(f"{GREEN}✔{RESET} 已更新 {updated_count} 筆資料庫紀錄。")

    print(f"\n{BLUE}✅ 優化完成！轉換: {converted}, 優化: {optimized}。{RESET}")

if __name__ == "__main__":
    optimize_images()
