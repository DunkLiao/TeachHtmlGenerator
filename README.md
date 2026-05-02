# TeachHtmlGenerator

TeachHtmlGenerator 是一個把文章檔案轉成靜態網站的小工具。你只要把文章放進 `source/` 資料夾，執行程式後，就會在 `output_html/` 產生可以用瀏覽器打開的網站。

這個工具適合用來整理教學文章、筆記、NotebookLM 回答內容，或任何想快速做成可瀏覽網頁的文字資料。

## 你可以用它做什麼

- 把多篇 `.txt` 或 `.md` 文章轉成 HTML 網頁
- 自動產生首頁與文章列表
- 在首頁用文章標題快速搜尋
- 自動產生文章摘要
- 自動建立文章目錄
- 支援 Markdown 常用格式
- 用設定檔調整首頁標題與網站配色

## 資料夾怎麼看

```text
TeachHtmlGenerator/
├─ source/               # 放原始文章
├─ output_html/          # 產生出來的網站
├─ generate_site.py      # 產生網站的主程式
├─ site_config.txt       # 一般使用者調整設定
├─ theme_options.py      # 內建配色方案定義
├─ style.css             # 網站樣式
├─ run.bat               # Windows 一鍵執行
└─ requirements.txt      # 需要安裝的 Python 套件
```

一般使用時，最常碰到的是這三個地方：

- `source/`：放文章
- `site_config.txt`：設定首頁標題與配色
- `run.bat`：產生網站

`output_html/` 是程式產生的結果，不建議直接手動修改。要改內容，請回到 `source/` 修改文章後重新產生。

## 快速開始

### 1. 安裝需要的套件

第一次使用前，請先安裝套件：

```powershell
python -m pip install -r requirements.txt
```

如果你使用 Windows，也可以先直接執行 `run.bat`。如果缺少套件，批次檔會提示你要執行哪一行安裝指令。

### 2. 放入文章

把文章放到 `source/` 資料夾。

支援的檔案格式：

- `.txt`
- `.md`

檔名會變成文章標題。例如：

```text
source/教我如何利用 AI 輔助寫 Excel 公式.md
```

產生後，文章頁標題會是：

```text
教我如何利用 AI 輔助寫 Excel 公式
```

### 3. 產生網站

Windows 使用者可以直接雙擊：

```text
run.bat
```

或在 PowerShell 執行：

```powershell
.\run.bat
```

也可以手動執行：

```powershell
python generate_site.py
```

成功後，網站會產生在：

```text
output_html/
```

請打開：

```text
output_html/index.html
```

## 如何修改首頁標題與配色

首頁標題與配色設定放在 `site_config.txt`。

預設配色為 `minimalist_bujo`。

打開檔案後，把第一個不是 `#` 開頭的文字行改成想使用的配色 key，並用 `site_title` 設定首頁標題：

```text
ocean_cyan
site_title=AI WITH EXCEL
```

首頁會顯示為：

```text
AI WITH EXCEL 教學資料彙整
```

改完後重新執行：

```powershell
.\run.bat
```

網站就會用新的首頁標題與配色重新產生。

### 可用配色

目前提供 13 種配色：

```text
classic_rose
slate_gold
forest_mint
ocean_cyan
indigo_lime
terracotta_sage
charcoal_coral
plum_amber
teal_copper
mono_blue
minimalist_bujo
notebook_ink
cyberpunk_presentation
```

配色只會改變顏色，不會改變文章排版、卡片大小、欄位數量或整體布局。

如果配色 key 寫錯，`run.bat` 會顯示錯誤並提示你回到 `site_config.txt` 檢查。

## 文章可以怎麼寫

文章內容支援常見 Markdown 寫法。

### 標題

```markdown
# 文章主標題

## 第一段

### 小節標題
```

文章頁會依照標題自動建立目錄。

### 段落與清單

```markdown
這是一段文字。

- 第一點
- 第二點
- 第三點
```

### 粗體、斜體、程式碼

```markdown
這是 **粗體**。
這是 *斜體*。
這是 `行內程式碼`。
```

### 表格

```markdown
| 項目 | 說明 |
| --- | --- |
| A | 第一個項目 |
| B | 第二個項目 |
```

### 待辦清單

```markdown
- [x] 已完成
- [ ] 尚未完成
```

## 產生出來的網站包含什麼

執行成功後，`output_html/` 會包含：

- `index.html`：首頁
- 每篇文章各自的 `.html` 頁面
- `style.css`：套用選定配色後的樣式檔

首頁會顯示：

- 網站標題
- 已收錄文章數量
- 文章搜尋欄
- 文章卡片列表

文章頁會顯示：

- 文章標題
- 自動摘要
- 返回首頁按鈕
- 文章目錄
- 文章正文
- 頁尾資訊

## run.bat 做了什麼

`run.bat` 是 Windows 的一鍵執行檔。它會自動做這些事：

1. 切換到專案資料夾
2. 尋找可用的 Python
3. 跳過 Windows Store 的 Python 假入口
4. 顯示目前選用的配色
5. 檢查配色設定是否正確
6. 檢查必要套件是否已安裝
7. 執行 `generate_site.py`
8. 產生 `output_html/index.html`

如果執行失敗，請先看畫面上的 `[ERROR]` 與 `[HINT]` 提示。

## 常見問題

### 我改了文章，但網頁沒有變

請確認你已經重新執行：

```powershell
.\run.bat
```

然後重新整理瀏覽器頁面。

### 我可以直接修改 output_html 裡的檔案嗎？

不建議。

`output_html/` 裡的檔案會在下次產生網站時被覆蓋。請修改 `source/` 裡的文章、`site_config.txt` 的首頁標題或配色，或 `style.css` 的樣式後重新產生。

### 中文檔名可以用嗎？

可以。

程式會保留中文、日文、韓文等常見 CJK 字元，並自動把不適合用在檔名的符號移除。

### 文章一定要用 Markdown 嗎？

不一定。

一般純文字也可以使用。Markdown 只是讓你可以加標題、清單、表格、粗體等格式。

### 首頁搜尋會搜尋文章內文嗎？

目前不會。

首頁搜尋只比對文章標題。

## 進階調整

### 修改網站樣式

如果要調整字體、間距、卡片樣式或其他畫面細節，請修改：

```text
style.css
```

如果只想改首頁標題或換顏色，請優先修改：

```text
site_config.txt
```

`theme_options.py` 是內建配色方案定義檔，通常不需要修改。

### 修改產生邏輯

如果要改文章排序、摘要規則、HTML 結構或頁尾內容，請修改：

```text
generate_site.py
```

## 手動檢查建議

每次修改後，建議檢查：

- `output_html/index.html` 是否有重新產生
- 首頁文章列表是否正常
- 至少一篇文章頁是否能打開
- 文章標題、摘要、目錄是否正常
- 中文檔名文章是否正常顯示
- 首頁標題是否符合 `site_config.txt`
- 選擇的配色是否已套用

## 已知限制

- 沒有後台管理介面
- 沒有資料庫
- 沒有自動化測試
- 首頁搜尋目前只搜尋文章標題
- 網站標題與頁尾文字目前寫在程式裡
- 原始 HTML 會被當成文字處理，不會直接當作 HTML 執行

## 作者

Dunk & Codex
