from __future__ import annotations

import html
import re
import shutil
import unicodedata
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable

try:
    from charset_normalizer import from_bytes
except ImportError:  # pragma: no cover - optional dependency
    from_bytes = None


ROOT_DIR = Path(__file__).resolve().parent
SOURCE_DIR = ROOT_DIR / "source"
OUTPUT_DIR = ROOT_DIR / "output_html"
STYLE_SOURCE = ROOT_DIR / "style.css"
STYLE_TARGET = OUTPUT_DIR / "style.css"

FOOTER_ITEMS = (
    ("免責申明", "基於公開資料，僅供參考，不構成建議"),
    ("資料來源", "網頁公開資訊"),
    ("版權所有", "© Dunk"),
)

TITLE_LINE_PATTERN = re.compile(r"^\s*\*\*(.+?)\*\*\s*$")
SAFE_NAME_PATTERN = re.compile(r"[^0-9A-Za-z\u4e00-\u9fff\u3040-\u30ff\uac00-\ud7af._ -]+")
WHITESPACE_PATTERN = re.compile(r"\s+")
SUMMARY_MAX_LENGTH = 120
BODY_PREVIEW_ROWS = 3
FALLBACK_ENCODINGS = ("utf-8", "utf-8-sig", "cp950", "big5", "gb18030")


@dataclass
class Section:
    title: str
    paragraphs: list[str]


@dataclass
class Article:
    source_name: str
    title: str
    output_name: str
    summary: str
    intro: list[str]
    sections: list[Section]


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


def split_paragraphs(text: str) -> list[str]:
    normalized = normalize_text(text)
    return [part.strip() for part in re.split(r"\n\s*\n", normalized) if part.strip()]


def parse_text_sections(text: str) -> tuple[list[str], list[Section], str]:
    lines = [line.strip() for line in normalize_text(text).splitlines()]
    intro: list[str] = []
    sections: list[Section] = []
    current_section: Section | None = None
    buffer: list[str] = []

    def flush_buffer() -> None:
        nonlocal buffer, current_section, intro
        paragraph = "\n".join(line for line in buffer if line).strip()
        buffer = []
        if not paragraph:
            return
        if current_section is None:
            intro.append(paragraph)
        else:
            current_section.paragraphs.append(paragraph)

    for line in lines:
        title_match = TITLE_LINE_PATTERN.match(line)
        if title_match:
            flush_buffer()
            current_section = Section(title=title_match.group(1).strip(), paragraphs=[])
            sections.append(current_section)
            continue

        if not line:
            flush_buffer()
            continue

        buffer.append(line)

    flush_buffer()

    sections = [section for section in sections if section.paragraphs]

    if not sections:
        fallback_paragraphs = intro or split_paragraphs(text)
        sections = [Section(title="內容重點", paragraphs=fallback_paragraphs)]
        intro = []

    summary_source = intro[0] if intro else sections[0].paragraphs[0]
    return intro, sections, summarize(summary_source)


def summarize(text: str, limit: int = SUMMARY_MAX_LENGTH) -> str:
    compact = " ".join(strip_formatting(text).split())
    if len(compact) <= limit:
        return compact
    return compact[: limit - 1].rstrip() + "…"


def summarize_cjk_friendly(text: str, limit: int) -> str:
    compact = " ".join(strip_formatting(text).split())
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


def escape_paragraphs(paragraphs: Iterable[str]) -> str:
    return "".join(f"<p>{render_inline(paragraph)}</p>" for paragraph in paragraphs)


def render_inline(text: str) -> str:
    escaped = html.escape(text)
    return re.sub(r"\*\*(.+?)\*\*", lambda match: f"<strong>{match.group(1)}</strong>", escaped)


def strip_formatting(text: str) -> str:
    return text.replace("**", "")


def build_preview_rows(lines: list[str]) -> str:
    if not lines:
        lines = ["來源檔案內容待整理", "此頁由文字檔自動轉換產生", "可於下方查看完整段落"]

    rows = []
    for index, line in enumerate(lines[:BODY_PREVIEW_ROWS], start=1):
        rows.append(
            f"""
              <div class="formula-row">
                <span class="cell">#{index}</span>
                <span>{html.escape(summarize(strip_formatting(line), 72))}</span>
              </div>"""
        )
    return "".join(rows)


def build_section_cards(sections: list[Section]) -> str:
    cards = []
    for index, section in enumerate(sections, start=1):
        cards.append(
            f"""
          <article class="step-card">
            <span class="icon" aria-hidden="true">{section_icon(index)}</span>
            <div>
              <p class="step-kicker">重點 {index:02d}</p>
              <h3>{html.escape(section.title)}</h3>
              {escape_paragraphs(section.paragraphs)}
            </div>
          </article>"""
        )
    return "".join(cards)


def build_article_html(article: Article) -> str:
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
          <h1>{html.escape(article.title)}</h1>
          <p>{html.escape(summarize_cjk_friendly(article.summary, 20))}</p>
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
        <div class="article-sections">
          {build_section_cards(article.sections)}
        </div>
      </section>
    </main>

    {build_footer()}
  </div>
</body>
</html>
"""


def build_index_html(articles: list[Article]) -> str:
    article_cards = "".join(
        f"""
          <article class="card article-card">
            <p class="step-kicker">文章 {index:02d}</p>
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
  <title>教學資料彙整</title>
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
          <h1>教學資料彙整</h1>
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
            <h2>教學資料彙整</h2>
          </div>
          <span class="source-tag">
            {doc_icon()}
          </span>
        </div>

        <div class="grid article-grid">
          {article_cards}
        </div>
      </section>
    </main>

    {build_footer()}
  </div>
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


def collect_articles() -> list[Article]:
    OUTPUT_DIR.mkdir(exist_ok=True)
    used_names: set[str] = set()
    articles: list[Article] = []

    for path in sorted(SOURCE_DIR.glob("*.txt")):
        text = read_text_with_detected_encoding(path)
        intro, sections, summary = parse_text_sections(text)
        output_name = slugify_filename(path.stem, used_names)
        articles.append(
            Article(
                source_name=path.name,
                title=path.stem,
                output_name=output_name,
                summary=summary,
                intro=intro,
                sections=sections,
            )
        )

    return articles


def write_output_files(articles: list[Article]) -> None:
    if STYLE_SOURCE.exists():
        shutil.copyfile(STYLE_SOURCE, STYLE_TARGET)

    index_html = build_index_html(articles)
    (OUTPUT_DIR / "index.html").write_text(index_html, encoding="utf-8")

    for article in articles:
        article_html = build_article_html(article)
        (OUTPUT_DIR / article.output_name).write_text(article_html, encoding="utf-8")


def main() -> None:
    if not SOURCE_DIR.exists():
        raise SystemExit("source directory not found")

    articles = collect_articles()
    write_output_files(articles)
    print(f"Generated {len(articles)} article page(s) in {OUTPUT_DIR}")


def section_icon(index: int) -> str:
    icons = (
        """<svg viewBox="0 0 24 24"><path d="M4 5h16"/><path d="M4 12h16"/><path d="M4 19h16"/><path d="M8 5v14"/><path d="M16 5v14"/></svg>""",
        """<svg viewBox="0 0 24 24"><path d="M9 11 12 14 22 4"/><path d="M21 12v7a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h11"/></svg>""",
        """<svg viewBox="0 0 24 24"><path d="M2 12s4-7 10-7 10 7 10 7-4 7-10 7S2 12 2 12Z"/><circle cx="12" cy="12" r="3"/></svg>""",
        """<svg viewBox="0 0 24 24"><path d="M12 20h9"/><path d="M16.5 3.5a2.1 2.1 0 0 1 3 3L7 19l-4 1 1-4Z"/></svg>""",
    )
    return icons[(index - 1) % len(icons)]


def band_icon() -> str:
    return """<svg viewBox="0 0 24 24"><path d="M12 9v4"/><path d="M12 17h.01"/><path d="M10.3 3.9 1.8 18a2 2 0 0 0 1.7 3h17a2 2 0 0 0 1.7-3L13.7 3.9a2 2 0 0 0-3.4 0Z"/></svg>"""


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
