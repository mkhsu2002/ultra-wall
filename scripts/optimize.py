#!/usr/bin/env python3
import os
import subprocess
import sys

# --- 色彩與標籤 ---
GREEN = "\033[92m"
BLUE = "\033[94m"
RESET = "\033[0m"

# --- 設定 ---
ASSETS_DIR = "assets"
MAX_WIDTH = 1600
QUALITY = 80 # 0-100

def optimize_images():
    print(f"{BLUE}🚀 開始優化 assets 中的圖檔...{RESET}")
    
    if not os.path.exists(ASSETS_DIR):
        print(f"找不到 {ASSETS_DIR} 資料夾。")
        return

    count = 0
    # 支援的副檔名
    valid_extensions = ('.png', '.jpg', '.jpeg', '.webp')

    for filename in os.listdir(ASSETS_DIR):
        if filename.lower().endswith(valid_extensions):
            filepath = os.path.join(ASSETS_DIR, filename)
            
            # 使用 macOS 內建的 sips 工具
            # 1. 限制最大寬度 (保持比例)
            # 2. 進行高品質壓縮
            try:
                # 取得原檔案大小
                old_size = os.path.getsize(filepath) / 1024
                
                # 執行 sips 指令
                subprocess.run([
                    "sips",
                    "--resampleWidth", str(MAX_WIDTH),
                    "-s", "formatOptions", str(QUALITY),
                    filepath
                ], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

                new_size = os.path.getsize(filepath) / 1024
                reduction = ((old_size - new_size) / old_size) * 100 if old_size > 0 else 0
                
                print(f"{GREEN}✔{RESET} {filename:30} | {old_size:7.1f}KB -> {new_size:7.1f}KB ({reduction:4.1f}% 節省)")
                count += 1
            except Exception as e:
                print(f"優化 {filename} 時發生錯誤: {e}")

    print(f"\n{BLUE}✅ 優化完成！共處理 {count} 張圖片。{RESET}")

if __name__ == "__main__":
    optimize_images()
