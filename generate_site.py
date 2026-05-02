from __future__ import annotations

import html
import re
import unicodedata
from dataclasses import dataclass
from pathlib import Path

from markdown_it import MarkdownIt
from markdown_it.token import Token
from mdit_py_plugins.tasklists import tasklists_plugin
from theme_options import ColorTheme, get_selected_theme
from theme_options import CONFIG_PATH as SITE_CONFIG_PATH

try:
    from charset_normalizer import from_bytes
except ImportError:  # pragma: no cover - optional dependency
    from_bytes = None


ROOT_DIR = Path(__file__).resolve().parent
SOURCE_DIR = ROOT_DIR / "source"
OUTPUT_DIR = ROOT_DIR / "output_html"
STYLE_SOURCE = ROOT_DIR / "style.css"
STYLE_TARGET = OUTPUT_DIR / "style.css"
SOURCE_PATTERNS = ("*.txt", "*.md")

FOOTER_ITEMS = (
    ("免責申明", "基於公開資料，僅供參考，不構成建議"),
    ("資料來源", "網頁公開資訊"),
    ("版權所有", "© Dunk"),
)

SAFE_NAME_PATTERN = re.compile(r"[^0-9A-Za-z\u4e00-\u9fff\u3040-\u30ff\uac00-\ud7af._ -]+")
WHITESPACE_PATTERN = re.compile(r"\s+")
SUMMARY_MAX_LENGTH = 120
BODY_PREVIEW_ROWS = 3
INDEX_TITLE_SUFFIX = "教學資料彙整"
FALLBACK_ENCODINGS = ("utf-8", "utf-8-sig", "cp950", "big5", "gb18030")
HTML_TAG_PATTERN = re.compile(r"<[^>]+>")
MARKDOWN_CONTROL_PATTERN = re.compile(r"[*_~`>#\[\]()!|:-]+")
CSS_ROOT_PATTERN = re.compile(r":root\s*\{.*?\}", re.DOTALL)
MARKDOWN_RENDERER = (
    MarkdownIt("gfm-like", {"html": False, "linkify": True, "typographer": False})
    .enable("table")
    .use(tasklists_plugin, enabled=True, label=True)
)


@dataclass
class TOCItem:
    level: int
    title: str
    anchor: str


@dataclass
class Article:
    source_name: str
    title: str
    output_name: str
    summary: str
    content_html: str
    toc_items: list[TOCItem]


@dataclass(frozen=True)
class SiteConfig:
    site_title: str = ""


def read_site_config() -> SiteConfig:
    if not SITE_CONFIG_PATH.exists():
        return SiteConfig()

    site_title = ""

    for line in SITE_CONFIG_PATH.read_text(encoding="utf-8").splitlines():
        value = line.strip()
        if not value or value.startswith("#") or "=" not in value:
            continue

        key, raw_value = value.split("=", 1)
        if key.strip().lower() == "site_title":
            site_title = raw_value.strip()

    return SiteConfig(site_title=site_title)


def build_index_title(site_title: str) -> str:
    title = site_title.strip()
    if not title:
        return INDEX_TITLE_SUFFIX
    return f"{title} {INDEX_TITLE_SUFFIX}"


def slugify_filename(name: str, used_names: set[str]) -> str:
    normalized = unicodedata.normalize("NFKC", name).strip()
    cleaned = SAFE_NAME_PATTERN.sub("", normalized)
    cleaned = WHITESPACE_PATTERN.sub("-", cleaned)
    cleaned = cleaned.strip(" .-_") or "document"
    candidate = f"{cleaned}.html"
    suffix = 2

    while candidate.lower() in used_names:
        candidate = f"{cleaned}-{suffix}.html"
        suffix += 1

    used_names.add(candidate.lower())
    return candidate


def read_text_with_detected_encoding(path: Path) -> str:
    raw = path.read_bytes()

    if from_bytes is not None:
        matches = from_bytes(raw)
        best_match = matches.best()
        if best_match is not None:
            return str(best_match)

    for encoding in FALLBACK_ENCODINGS:
        try:
            return raw.decode(encoding)
        except UnicodeDecodeError:
            continue

    return raw.decode("utf-8", errors="replace")


def normalize_text(text: str) -> str:
    return text.replace("\r\n", "\n").replace("\r", "\n").replace("\ufeff", "")


def summarize(text: str, limit: int = SUMMARY_MAX_LENGTH) -> str:
    compact = " ".join(strip_markdown(text).split())
    if len(compact) <= limit:
        return compact
    return compact[: limit - 1].rstrip() + "…"


def summarize_cjk_friendly(text: str, limit: int) -> str:
    compact = " ".join(strip_markdown(text).split())
    if not compact:
        return ""

    count = 0
    result: list[str] = []

    for char in compact:
        next_count = count + (2 if is_cjk_char(char) else 1)
        if next_count > limit:
            break
        result.append(char)
        count = next_count

    summary = "".join(result).rstrip()
    if len(summary) == len(compact):
        return summary

    summary = re.sub(r"[A-Za-z0-9]+$", "", summary).rstrip(" -_/.,;:")
    if not summary:
        summary = compact[:limit].rstrip()
    return summary + "…"


def is_cjk_char(char: str) -> bool:
    code = ord(char)
    return (
        0x4E00 <= code <= 0x9FFF
        or 0x3400 <= code <= 0x4DBF
        or 0x3040 <= code <= 0x30FF
        or 0xAC00 <= code <= 0xD7AF
    )


def make_slug(value: str, used_slugs: set[str]) -> str:
    normalized = unicodedata.normalize("NFKC", strip_markdown(value)).strip().lower()
    normalized = normalized.replace(" ", "-")
    cleaned = SAFE_NAME_PATTERN.sub("", normalized)
    cleaned = WHITESPACE_PATTERN.sub("-", cleaned).strip(" .-_") or "section"
    candidate = cleaned
    suffix = 2

    while candidate in used_slugs:
        candidate = f"{cleaned}-{suffix}"
        suffix += 1

    used_slugs.add(candidate)
    return candidate


def escape_raw_html(text: str) -> str:
    return html.escape(text, quote=False)


def strip_markdown(text: str) -> str:
    normalized = normalize_text(text)
    escaped = escape_raw_html(normalized)
    rendered = MARKDOWN_RENDERER.render(escaped)
    without_tags = HTML_TAG_PATTERN.sub(" ", rendered)
    decoded = html.unescape(without_tags)
    cleaned = MARKDOWN_CONTROL_PATTERN.sub(" ", decoded)
    cleaned = WHITESPACE_PATTERN.sub(" ", cleaned)
    return cleaned.strip()


def extract_inline_text(token: Token) -> str:
    if token.type == "text":
        return token.content
    if token.type == "code_inline":
        return token.content
    if token.type == "image":
        return token.content or token.attrGet("alt") or ""
    if token.children:
        return "".join(extract_inline_text(child) for child in token.children)
    return token.content or ""


def extract_heading_text(tokens: list[Token], heading_index: int) -> str:
    if heading_index + 1 >= len(tokens):
        return ""
    inline_token = tokens[heading_index + 1]
    return extract_inline_text(inline_token).strip()


def collect_toc_items(tokens: list[Token], used_slugs: set[str]) -> list[TOCItem]:
    toc_items: list[TOCItem] = []

    for index, token in enumerate(tokens):
        if token.type != "heading_open":
            continue

        level = int(token.tag[1:])
        title = strip_markdown(extract_heading_text(tokens, index))
        if not title:
            continue

        anchor = make_slug(title, used_slugs)
        token.attrSet("id", anchor)

        if level >= 2:
            toc_items.append(TOCItem(level=level, title=title, anchor=anchor))

    return toc_items


def find_summary_source(tokens: list[Token]) -> str:
    for index, token in enumerate(tokens):
        if token.type != "inline":
            continue
        if index > 0 and tokens[index - 1].type == "heading_open":
            continue

        plain = strip_markdown(extract_inline_text(token))
        if plain:
            return plain

    return "來源檔案內容待整理"


def render_markdown_document(text: str) -> tuple[str, list[TOCItem], str]:
    normalized = normalize_text(text)
    escaped = escape_raw_html(normalized)
    tokens = MARKDOWN_RENDERER.parse(escaped)
    toc_items = collect_toc_items(tokens, used_slugs=set())
    summary = summarize(find_summary_source(tokens))
    content_html = MARKDOWN_RENDERER.renderer.render(tokens, MARKDOWN_RENDERER.options, {})
    content_html = content_html.strip() or "<p>來源檔案內容待整理。</p>"
    return content_html, toc_items, summary


def build_preview_rows(lines: list[str]) -> str:
    if not lines:
        lines = ["來源檔案內容待整理", "此頁由文字檔自動轉換產生", "可於下方查看完整段落"]

    rows = []
    for index, line in enumerate(lines[:BODY_PREVIEW_ROWS], start=1):
        rows.append(
            f"""
              <div class="formula-row">
                <span class="cell">#{index}</span>
                <span>{html.escape(summarize(strip_markdown(line), 72))}</span>
              </div>"""
        )
    return "".join(rows)


def build_table_of_contents(toc_items: list[TOCItem]) -> str:
    if not toc_items:
        return ""

    links = "".join(
        f"""
            <li class="toc-level-{item.level}">
              <a href="#{html.escape(item.anchor, quote=True)}">{html.escape(item.title)}</a>
            </li>"""
        for item in toc_items
    )

    return f"""
        <aside class="article-toc">
          <p class="toc-label">文章目錄</p>
          <ol>
            {links}
          </ol>
        </aside>"""


def build_article_html(article: Article) -> str:
    table_of_contents = build_table_of_contents(article.toc_items)
    layout_class = "article-layout with-toc" if article.toc_items else "article-layout"

    return f"""<!doctype html>
<html lang="zh-Hant">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{html.escape(article.title)}</title>
  <link rel="stylesheet" href="./style.css">
</head>
<body>
  <div class="site-shell">
    <header class="hero">
      <div class="hero-inner article-hero-inner">
        <div>
          <p class="eyebrow">
            {doc_icon()}
            教學文章
          </p>
          <h1>{html.escape(article.title)}</h1>
          <p>{html.escape(summarize_cjk_friendly(article.summary, 52))}</p>
          <div class="hero-actions">
            <a class="button" href="./index.html">
              {arrow_left_icon()}
              返回索引
            </a>
          </div>
        </div>
      </div>
    </header>

    <main>
      <section class="content article-content" id="article-content">
        <div class="{layout_class}">
          {table_of_contents}
          <article class="markdown-body article-panel">
            {article.content_html}
          </article>
        </div>
      </section>
    </main>

    {build_footer()}
  </div>
</body>
</html>
"""


def build_index_html(articles: list[Article], config: SiteConfig) -> str:
    index_title = build_index_title(config.site_title)
    article_cards = "".join(
        f"""
          <article class="card article-card" data-title="{html.escape(article.title, quote=True)}">
            <p class="step-kicker">文章 {index:03d}</p>
            <h3>{html.escape(article.title)}</h3>
            <p class="article-card-summary">{html.escape(summarize_cjk_friendly(article.summary, 48))}</p>
            <div class="article-card-meta">
              <span class="source-tag" aria-label="來源檔案">{doc_icon()}</span>
            </div>
            <a class="button article-link" href="./{html.escape(article.output_name)}">
              {arrow_right_icon()}
              開啟文章
            </a>
          </article>"""
        for index, article in enumerate(articles, start=1)
    )

    return f"""<!doctype html>
<html lang="zh-Hant">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{html.escape(index_title)}</title>
  <link rel="stylesheet" href="./style.css">
</head>
<body>
  <div class="site-shell">
    <header class="hero">
      <div class="hero-inner">
        <div>
          <p class="eyebrow">
            {spark_icon()}
            首頁
          </p>
          <h1>{html.escape(index_title)}</h1>
          <div class="hero-actions">
            <a class="button" href="#article-list">
              {arrow_right_icon()}
              查看文章
            </a>
            <span class="button secondary article-meta-pill">
              {doc_icon()}
              已收錄 {len(articles)} 篇
            </span>
          </div>
        </div>

        <aside class="hero-visual" aria-label="索引摘要示意">
          <div class="mock-window">
            <div class="mock-bar" aria-hidden="true">
              <span class="mock-dot"></span>
              <span class="mock-dot"></span>
              <span class="mock-dot"></span>
            </div>
            <div class="formula-card">
              {build_index_preview_rows(articles)}
            </div>
          </div>
        </aside>
      </div>
    </header>

    <main>
      <section class="content" id="article-list">
        <div class="section-head">
          <div>
            <h2>{html.escape(index_title)}</h2>
            <p>輸入文章標題關鍵字，立即篩選符合的教學內容。</p>
          </div>
          <span class="source-tag">
            {doc_icon()}
          </span>
        </div>

        <div class="search-panel">
          <label class="search-label" for="article-search">搜尋文章標題</label>
          <input
            id="article-search"
            class="search-input"
            type="search"
            placeholder="請輸入您要查詢的關鍵字"
            autocomplete="off"
            spellcheck="false"
          >
        </div>

        <div class="grid article-grid">
          {article_cards}
        </div>
        <p class="search-empty" id="search-empty" hidden>找不到符合這個關鍵字的文章標題。</p>
      </section>
    </main>

    {build_footer()}
  </div>
  <script>
    document.addEventListener("DOMContentLoaded", () => {{
      const searchInput = document.getElementById("article-search");
      const emptyState = document.getElementById("search-empty");
      const articleCards = Array.from(document.querySelectorAll(".article-card"));

      if (!searchInput || !emptyState || articleCards.length === 0) {{
        return;
      }}

      const normalize = (value) => String(value || "").trim().toLowerCase();

      const updateResults = () => {{
        const query = normalize(searchInput.value);
        let visibleCount = 0;

        for (const card of articleCards) {{
          const titleElement = card.querySelector("h3");
          const title = normalize(titleElement ? titleElement.textContent : card.dataset.title);
          const isMatch = query === "" || title.indexOf(query) !== -1;

          card.style.display = isMatch ? "" : "none";
          if (isMatch) {{
            visibleCount += 1;
          }}
        }}

        emptyState.style.display = visibleCount === 0 ? "block" : "none";
      }};

      searchInput.addEventListener("input", updateResults);
      searchInput.addEventListener("search", updateResults);
      updateResults();
    }});
  </script>
</body>
</html>
"""


def build_index_preview_rows(articles: list[Article]) -> str:
    lines = [article.title for article in articles[:BODY_PREVIEW_ROWS]]
    return build_preview_rows(lines)


def build_footer() -> str:
    items = "".join(
        f"""
        <div class="footer-item">
          <span class="footer-label">{html.escape(label)}</span>
          {html.escape(value)}
        </div>"""
        for label, value in FOOTER_ITEMS
    )
    return f"""
    <footer class="site-footer">
      <div class="footer-inner">{items}
      </div>
    </footer>"""


def build_theme_root_css(theme: ColorTheme) -> str:
    variables = "\n".join(
        f"  {name}: {value};"
        for name, value in sorted(theme.variables.items())
    )
    return f":root {{\n{variables}\n  --radius: 8px;\n}}"


def build_themed_stylesheet(theme: ColorTheme) -> str:
    stylesheet = STYLE_SOURCE.read_text(encoding="utf-8")
    theme_root = build_theme_root_css(theme)

    if CSS_ROOT_PATTERN.search(stylesheet):
        return CSS_ROOT_PATTERN.sub(theme_root, stylesheet, count=1)

    return f"{theme_root}\n\n{stylesheet}"


def collect_articles() -> list[Article]:
    OUTPUT_DIR.mkdir(exist_ok=True)
    used_names: set[str] = set()
    articles: list[Article] = []

    source_paths = [
        path
        for pattern in SOURCE_PATTERNS
        for path in SOURCE_DIR.glob(pattern)
    ]

    for path in sorted(source_paths, key=lambda item: (item.stat().st_mtime, item.name.lower())):
        text = read_text_with_detected_encoding(path)
        content_html, toc_items, summary = render_markdown_document(text)
        output_name = slugify_filename(path.stem, used_names)
        articles.append(
            Article(
                source_name=path.name,
                title=path.stem,
                output_name=output_name,
                summary=summary,
                content_html=content_html,
                toc_items=toc_items,
            )
        )

    return articles


def write_output_files(articles: list[Article], theme: ColorTheme, config: SiteConfig) -> None:
    if STYLE_SOURCE.exists():
        STYLE_TARGET.write_text(build_themed_stylesheet(theme), encoding="utf-8")

    index_html = build_index_html(articles, config)
    (OUTPUT_DIR / "index.html").write_text(index_html, encoding="utf-8")

    for article in articles:
        article_html = build_article_html(article)
        (OUTPUT_DIR / article.output_name).write_text(article_html, encoding="utf-8")


def main() -> None:
    if not SOURCE_DIR.exists():
        raise SystemExit("source directory not found")

    try:
        theme = get_selected_theme()
    except ValueError as exc:
        raise SystemExit(str(exc)) from exc

    config = read_site_config()
    articles = collect_articles()
    write_output_files(articles, theme, config)
    print(f"Generated {len(articles)} article page(s) in {OUTPUT_DIR}")
    print(f"Theme: {theme.name}")
    print(f"Index title: {build_index_title(config.site_title)}")


def spark_icon() -> str:
    return """<svg aria-hidden="true" viewBox="0 0 24 24"><path d="M12 3v3"/><path d="M18.4 5.6l-2.1 2.1"/><path d="M21 12h-3"/><path d="M5.6 5.6l2.1 2.1"/><path d="M3 12h3"/><path d="M12 21v-4"/><path d="M8 14a4 4 0 1 1 8 0c0 1.3-.8 2.4-1.8 3H9.8C8.8 16.4 8 15.3 8 14Z"/></svg>"""


def doc_icon() -> str:
    return """<svg aria-hidden="true" viewBox="0 0 24 24"><path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8Z"/><path d="M14 2v6h6"/><path d="M8 13h8"/><path d="M8 17h5"/></svg>"""


def arrow_right_icon() -> str:
    return """<svg aria-hidden="true" viewBox="0 0 24 24"><path d="M5 12h14"/><path d="m13 6 6 6-6 6"/></svg>"""


def arrow_left_icon() -> str:
    return """<svg aria-hidden="true" viewBox="0 0 24 24"><path d="M19 12H5"/><path d="m11 18-6-6 6-6"/></svg>"""


if __name__ == "__main__":
    main()
