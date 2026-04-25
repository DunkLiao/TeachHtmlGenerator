# TeachHtmlGenerator

`TeachHtmlGenerator` 是一個用 Python 撰寫的靜態網站產生器，會把 `source/` 裡的教學文章純文字檔轉成可直接瀏覽的 HTML 網站。

目前專案的定位很明確：

- 輸入是 `source/*.txt`
- 輸出是 `output_html/*.html` 與 `output_html/style.css`
- 不依賴後端框架、資料庫或前端打包工具
- 以繁體中文內容與 CJK 顯示為主要使用情境

## 專案目的

這個專案適合用在以下情境：

- 將一批教學文章快速整理成可瀏覽的靜態網站
- 用最少依賴維持可讀性高的 HTML 輸出
- 讓非工程背景的人也能只靠編輯 `.txt` 檔更新內容
- 文字檔來源：詢問notebooklm的回答結果。

## 目前功能

- 自動讀取 `source/` 內所有 `.txt` 文章
- 依檔名產生頁面標題與輸出檔名
- 支援 Markdown 與常見 GFM 語法輸出
- 自動建立文章頁目錄錨點
- 首頁提供文章標題即時搜尋
- 自動產生摘要並套用 CJK 友善截斷
- 複製共用樣式到輸出目錄

## 技術棧

### 生成端

- Python 3
- Python 標準函式庫
  - `pathlib`
  - `dataclasses`
  - `re`
  - `html`
  - `shutil`
  - `unicodedata`
- `charset-normalizer`
  - 改善來源文字編碼辨識
- `markdown-it-py`
  - 將文章內容解析成 HTML
- `mdit-py-plugins`
  - 啟用 task list 等延伸語法
- `linkify-it-py`
  - 支援自動連結辨識

### 前端輸出

- 純 HTML5
- 單一共享樣式檔 [`style.css`](D:/SourceCode/VibeCoding/TeachHtmlGenerator/style.css)
- 首頁少量原生 JavaScript，用於前端搜尋過濾
- 原生 SVG icon 直接內嵌在 HTML 中

## 專案結構

```text
TeachHtmlGenerator/
├─ generate_site.py      # 主程式：讀取來源、轉成 HTML、輸出網站
├─ style.css             # 共用樣式
├─ run.bat               # Windows 執行入口
├─ requirements.txt      # 專案依賴
├─ source/               # 文章來源 .txt
└─ output_html/          # 生成後網站輸出
```

## 安裝與執行

先安裝依賴：

```powershell
python -m pip install -r requirements.txt
```

再產生網站：

```powershell
python generate_site.py
```

Windows 也可以直接使用：

```powershell
run.bat
```

成功後會在 `output_html/` 看到：

- `index.html`
- 每篇文章對應的 `.html`
- `style.css`

## 生成流程

核心邏輯集中在 [`generate_site.py`](D:/SourceCode/VibeCoding/TeachHtmlGenerator/generate_site.py)：

1. 掃描 `source/` 內所有 `.txt`
2. 嘗試偵測並讀取文字編碼
3. 正規化換行與 BOM
4. 以 Markdown/GFM 規則解析內容
5. 建立文章摘要與目錄錨點
6. 依原始檔名產生安全輸出檔名
7. 輸出 `index.html` 與各文章頁
8. 複製 `style.css` 到 `output_html/`

## 文字檔格式

目前文章內容不是走舊版的自訂 `**章節**` 規則，而是直接交給 Markdown 解析器處理。

可用的內容形式包含：

- 段落
- 標題 `#`、`##`、`###`
- 粗體、斜體、行內程式碼
- 清單與核取方塊
- 表格
- 自動連結

HTML 原始碼不會直接放行；程式會先 escape 再交給 Markdown renderer，因此來源文字會以較保守、安全的方式輸出。

## 摘要與文章目錄

摘要會從文章中第一個可讀文字區塊擷取，再做長度裁切。

- 一般摘要邏輯使用 `summarize()`
- 首頁與文章頁顯示時會再使用 `summarize_cjk_friendly()`，避免中日韓文字被截得太難看

文章內容中的標題會自動建立錨點 `id`，並在文章頁右側或上方顯示「文章目錄」。

- 所有標題都會被賦予錨點
- `h2` 以上層級會進入 TOC 清單
- 相同標題會自動補 `-2`、`-3` 避免衝突

## 檔名與輸出規則

來源檔名會同時影響文章標題與輸出檔名。

- 檔名去掉副檔名後，直接作為文章標題
- 會經過 Unicode `NFKC` 正規化
- 允許英數字、CJK、日文、韓文、`.`、`_`、空白、`-`
- 多個空白會壓成單一 `-`
- 會補上 `.html`
- 若重名，會自動加上 `-2`、`-3` 等尾碼

因此中文檔名可直接保留，不需要另外手動轉 slug。

## 編碼處理

讀取來源文字時，程式會優先使用 `charset-normalizer` 偵測；若不可用，則退回以下編碼依序嘗試：

- `utf-8`
- `utf-8-sig`
- `cp950`
- `big5`
- `gb18030`

若全部失敗，最後會用 `utf-8` 加上 `errors="replace"` 兜底。

## 輸出頁面

### 首頁 `index.html`

首頁目前包含：

- 站點主視覺區塊
- 已收錄文章數
- 文章標題搜尋欄
- 文章卡片列表

搜尋是前端即時過濾，依標題文字比對，不需要後端。

### 文章頁

每篇文章頁目前包含：

- 文章標題
- 文章摘要
- 返回首頁按鈕
- 文章目錄
- Markdown 轉換後的正文內容
- 固定頁尾資訊

## `run.bat` 行為

[`run.bat`](D:/SourceCode/VibeCoding/TeachHtmlGenerator/run.bat) 的流程是：

1. 切換到專案目錄
2. 優先找 `D:\ProgramData\anaconda3\python.exe`
3. 找不到再用 `where python`
4. 執行 `generate_site.py`
5. 顯示成功或失敗訊息

這個批次檔偏向 Windows 本機使用情境。

## 開發說明

### 日常更新內容

如果只是新增或修改文章，通常只需要：

1. 編輯 `source/*.txt`
2. 執行 `python generate_site.py`
3. 檢查 `output_html/index.html` 與文章頁

### 調整樣式

請修改 [`style.css`](D:/SourceCode/VibeCoding/TeachHtmlGenerator/style.css)。

### 調整生成邏輯

請修改 [`generate_site.py`](D:/SourceCode/VibeCoding/TeachHtmlGenerator/generate_site.py)。

### 不建議直接修改輸出檔

`output_html/` 是生成產物，除錯以外不建議直接手改。

## 手動驗證

目前沒有自動化測試；每次修改後建議至少執行：

```powershell
python generate_site.py
```

然後確認：

- `output_html/index.html` 已重新產生
- 至少開一篇文章頁，確認標題、摘要、Markdown 內容與目錄正常
- 至少檢查一篇非 ASCII / 中文檔名來源文章

## 已知限制

- 沒有自動化測試
- 沒有 CLI 參數，輸入與輸出目錄目前固定
- 首頁搜尋只比對文章標題，不搜尋內文
- 站點標題與 footer 內容目前寫死在程式常數中
- 來源文字中的原始 HTML 不會直接當作 HTML 輸出

## 後續可擴充方向

- 加入 `pytest` 測試
- 將站點標題、footer 文案改為可設定
- 增加 CLI 參數，例如自訂輸入輸出路徑
- 支援文章標籤、分類或排序選項
- 增加 sitemap、Open Graph 或其他 metadata
- 補上內容全文搜尋

## 授權與產物說明

- `source/`：內容來源
- `output_html/`：生成產物
- 請優先修改來源或模板程式，再重新生成

## 作者

Dunk & CODEX
