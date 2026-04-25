# TeachHtmlGenerator

`TeachHtmlGenerator` 是一個用 Python 撰寫的靜態網站產生器，專門把 `source/` 裡的教學文章純文字檔轉成一個可直接瀏覽的 HTML 小型網站。

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

## 技術棧

### 後端 / 生成端

- Python 3
- Python 標準函式庫
  - `pathlib`：路徑處理
  - `dataclasses`：文章與段落資料模型
  - `re`：文字解析與檔名清理
  - `html`：HTML escape
  - `shutil`：複製樣式檔
  - `unicodedata`：檔名正規化
- `charset-normalizer`（可選）
  - 用來提升 `.txt` 來源檔的編碼辨識能力

### 前端輸出

- 純 HTML5
- 單一共享 CSS 檔：[`style.css`](D:/SourceCode/VibeCoding/TeachHtmlGenerator/style.css)
- 原生 SVG icon 內嵌在 HTML 中
- 無 JavaScript

## 專案結構

```text
TeachHtmlGenerator/
├─ generate_site.py      # 主程式：讀取文字、解析文章、輸出 HTML
├─ style.css             # 共用樣式
├─ run.bat               # Windows 執行入口
├─ requirements.txt      # 可選依賴
├─ source/               # 文章來源 .txt
└─ output_html/          # 產生後的網站輸出
```

## 執行方式

### 1. 安裝依賴

```powershell
python -m pip install -r requirements.txt
```

`requirements.txt` 目前只有一個可選套件：

```text
charset-normalizer>=3.3,<4
```

就算沒安裝，程式仍可執行，只是會退回內建的多組編碼嘗試。

### 2. 產生網站

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

## 整體流程

專案流程很單純，核心都在 [`generate_site.py`](D:/SourceCode/VibeCoding/TeachHtmlGenerator/generate_site.py)：

1. 讀取 `source/` 下所有 `.txt` 檔
2. 自動偵測文字編碼
3. 正規化換行與 BOM
4. 解析文章前言與分節內容
5. 產生摘要
6. 將原始檔名轉成安全的輸出檔名
7. 產出 `index.html` 與各文章頁
8. 複製 `style.css` 到 `output_html/`

## 文字檔格式規則

這個生成器支援的文章格式不是 Markdown 全語法，而是「簡化規則」。

### 1. 檔名

- `source` 內每個 `.txt` 檔都代表一篇文章
- 檔名（不含副檔名）會直接作為文章標題
- 同時也會作為輸出頁面的 slug 基礎

例如：

```text
source/教我如何利用 AI 輔助寫出複雜的 Excel 公式？.txt
```

會變成類似：

```text
output_html/教我如何利用-AI-輔助寫出複雜的-Excel-公式.html
```

### 2. 分段

- 空白行會切出新段落
- 連續文字會被視為同一段

### 3. 章節標題

符合這個格式的單行文字會被視為一個 section 標題：

```text
**章節標題**
```

例如：

```text
**第一步：先讓 AI 看懂資料的結構**
```

### 4. 粗體

內文中的 `**文字**` 會轉成 `<strong>`

例如：

```text
請先確認 **每一欄的用途** 是否一致。
```

### 5. 沒有章節標題時

如果整篇文章完全沒有 `**章節標題**` 這種分節格式，程式會自動建立一個預設章節：

- 標題：`內容重點`

## 實際解析邏輯

### intro 與 sections

程式會把第一個 section 標題之前的段落當成 `intro`，之後每個 `**標題**` 區塊視為一個 section。

但目前輸出的文章頁只渲染 `sections`，不單獨顯示 `intro` 區塊；`intro` 主要用於摘要來源判定。

### 摘要產生

摘要來源規則如下：

- 有 `intro` 時，優先取 `intro[0]`
- 否則取第一個 section 的第一段

另外專案有兩種摘要策略：

- `summarize()`：一般長度裁切
- `summarize_cjk_friendly()`：對中日韓字元較友善，避免截斷觀感太差

首頁與文章頁都使用了偏向 CJK 顯示友善的摘要版本。

## 檔名與 slug 規則

檔名處理邏輯包含幾件事：

- 使用 Unicode `NFKC` 正規化
- 保留英數字、CJK、日文、韓文、`.`、`_`、空白、`-`
- 多個空白壓成單一 `-`
- 去除前後多餘符號
- 自動補上 `.html`
- 若重名，會加上 `-2`、`-3` 這類尾碼

因此它對中文檔名是友善的，不會強制轉成拼音或 ASCII slug。

## 編碼處理

來源文字會先走 `charset-normalizer` 偵測；若套件不存在，則退回這些編碼逐一嘗試：

- `utf-8`
- `utf-8-sig`
- `cp950`
- `big5`
- `gb18030`

如果都失敗，最後會用 `utf-8` 搭配 `errors="replace"` 兜底。

這使得專案對繁中常見文字來源相對寬容。

## 產出頁面說明

### 首頁 `index.html`

首頁會列出所有文章卡片，包含：

- 文章標題
- 短摘要
- 文章連結
- 已收錄篇數

### 文章頁

每篇文章頁會顯示：

- 文章標題
- 簡短摘要
- section 卡片列表
- 返回首頁按鈕
- 固定頁尾資訊

## 樣式設計

樣式集中在 [`style.css`](D:/SourceCode/VibeCoding/TeachHtmlGenerator/style.css)，目前特徵如下：

- 暖色系品牌配色
- 單欄閱讀式文章頁
- 卡片式 section 呈現
- 固定底部 footer
- 響應式設計，針對 `860px` 與 `520px` 有斷點
- 以 `Noto Sans TC` / `Microsoft JhengHei` 等中文字型優先

## `run.bat` 行為

[`run.bat`](D:/SourceCode/VibeCoding/TeachHtmlGenerator/run.bat) 是 Windows 方便執行入口，流程是：

1. 切換到專案目錄
2. 優先找 `D:\ProgramData\anaconda3\python.exe`
3. 找不到再用 `where python`
4. 執行 `generate_site.py`
5. 顯示成功或失敗訊息

這代表它目前偏向 Windows 本機使用情境，而且對特定 Anaconda 路徑有優先支援。

## 開發與維護建議

### 日常更新內容

如果你只是要新增或修改文章，通常只需要：

1. 編輯 `source/*.txt`
2. 執行 `python generate_site.py`
3. 檢查 `output_html/index.html` 與文章頁

### 調整版面

若要改外觀，請修改：

- [`style.css`](D:/SourceCode/VibeCoding/TeachHtmlGenerator/style.css)

### 調整解析規則

若要改文章格式、摘要、slug 或輸出 HTML 結構，請修改：

- [`generate_site.py`](D:/SourceCode/VibeCoding/TeachHtmlGenerator/generate_site.py)

### 不建議直接修改輸出檔

`output_html/` 是產物目錄，除錯以外不建議手改。

## 手動驗證

目前沒有自動化測試；每次修改後建議至少做這些檢查：

```powershell
python generate_site.py
```

然後確認：

- `output_html/index.html` 已重新產生
- 至少開一篇文章頁，確認標題、摘要、section 內容正確
- 至少檢查一篇非 ASCII / 中文檔名來源文章

## 已知限制

- 不是完整 Markdown parser
- 不支援圖片、清單、表格、程式碼區塊
- `intro` 目前會參與摘要判定，但不會獨立渲染在文章頁
- 頁尾文案寫死在程式常數中
- 沒有自動化測試
- 沒有 CLI 參數，輸入輸出目錄目前固定

## 後續可擴充方向

- 加入 `pytest` 測試
- 支援更多文字語法，例如清單或引用
- 將站點標題、footer 文案改為可設定
- 增加 CLI 參數，例如自訂輸入輸出路徑
- 讓文章頁顯示 `intro`
- 產生 sitemap 或 metadata

## 授權與產物說明

- `source/`：內容來源
- `output_html/`：生成產物
- 請優先修改來源或模板程式，再重新生成

## 作者
Dunk & CODEX

