# AI 電商行銷設計師 Ultra 作品集展示牆 (Ultra Showcase)

這是一個為「AI 電商行銷設計師 Ultra」打造的高級 SaaS 風格作品展示網站。採用 Apple 官網美學與 Pinterest 沉浸式石板街 (Masonry) 佈局，專為展示 AI 生成的電商素材、網頁設計及品牌提案而生。

![Preview](https://images.unsplash.com/photo-1556228720-195a672e8a03?auto=format&fit=crop&q=80&w=800)

## ✨ 特色功能

- **Pinterest 沉浸式佈局**：自適應多欄石板街設計，讓作品填滿整個畫面，提供絕佳視覺衝擊。
- **動態分類與搜尋**：具備即時關鍵字搜尋與分類標籤過濾功能，快速找到特定類別的作品。
- **免伺服器後台 (Decap CMS)**：內建管理後台，讓您直接在瀏覽器上傳圖片與管理作品，無需動動程式碼。
- **本地圖片優化工具**：內建 Python 腳本，一鍵壓縮並調整圖檔尺寸，確保網站載入飛快。
- **100% 靜態部署**：極輕量化，完美支援 Cloudflare Pages 或 GitHub Pages。

## 🚀 快速開始

### 本地預覽
1. 下載或克隆本倉庫。
2. 在根目錄執行簡易伺服器：
   ```bash
   python3 -m http.server 8000
   ```
3. 在瀏覽器打開 `http://localhost:8000`。

### 圖片優化
如果您手動新增了高畫質圖檔到 `assets/` 資料夾，請執行以下指令進行自動優化：
```bash
python3 scripts/optimize.py
```

## 🛠️ 管理後台使用說明

網站部署至 Cloudflare Pages 後，您可以訪問：
`https://您的網址.com/admin`

1. 使用您的 GitHub 帳號登入。
2. 在「作品管理」中點擊「新增」。
3. 上傳圖片、填寫標題並選擇分類。
4. 點擊「發佈」，網站將在幾分鐘內自動更新內容。

## 📂 專案架構

- `index.html`: 網站核心結構。
- `style.css`: Pinterest 各式風格與響應式定義。
- `main.js`: 動態載入、搜尋與燈箱邏輯。
- `data/works.json`: 作品清單資料庫。
- `admin/`: 管理後台設定。
- `scripts/`: 本地維護工具。

## 📝 授權

本專案僅供作品展示使用，作品著作權歸其創作者所有。
