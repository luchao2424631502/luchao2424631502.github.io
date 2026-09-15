#!/usr/bin/env python3
"""Recover Hexo Markdown sources from a generated Fluid static site in Git."""

from __future__ import annotations

import argparse
import hashlib
import re
import subprocess
from datetime import datetime
from pathlib import Path

import yaml
from bs4 import BeautifulSoup, NavigableString, Tag
from markdownify import markdownify


POST_PATH = re.compile(r"^(\d{4})/(\d{2})/(\d{2})/(.+)/index\.html$")
LANGUAGE_MAP = {
    "c++": "cpp",
    "c#": "csharp",
    "js": "javascript",
    "py": "python",
    "sh": "bash",
    "shell": "bash",
    "yml": "yaml",
}


def git(repo: Path, *args: str) -> bytes:
    return subprocess.check_output(["git", "-C", str(repo), *args])


def git_paths(repo: Path, revision: str) -> list[str]:
    raw = git(repo, "-c", "core.quotePath=false", "ls-tree", "-rz", "--name-only", revision)
    return [item.decode("utf-8") for item in raw.split(b"\0") if item]


def git_text(repo: Path, revision: str, path: str) -> str:
    return git(repo, "show", f"{revision}:{path}").decode("utf-8", errors="replace")


def text_or_none(node: Tag | None) -> str | None:
    if node is None:
        return None
    value = node.get_text(" ", strip=True)
    return value or None


def recover_title(soup: BeautifulSoup, slug: str) -> str:
    candidates = [
        soup.select_one("article.post-content h1"),
        soup.select_one("#subtitle[title]"),
        soup.select_one('meta[property="og:title"]'),
    ]
    for node in candidates:
        if node is None:
            continue
        if node.name == "meta":
            value = node.get("content")
        elif node.has_attr("title"):
            value = node.get("title")
        else:
            value = text_or_none(node)
        if value:
            return str(value).strip()
    return slug


def recover_date(soup: BeautifulSoup, year: str, month: str, day: str) -> str:
    node = soup.select_one("time[datetime]")
    value = str(node.get("datetime", "")).strip() if node else ""
    for pattern in ("%Y-%m-%d %H:%M", "%Y-%m-%d %H:%M:%S", "%Y-%m-%d"):
        try:
            parsed = datetime.strptime(value, pattern)
            return parsed.strftime("%Y-%m-%d %H:%M:%S")
        except ValueError:
            pass
    return f"{year}-{month}-{day} 00:00:00"


def recover_taxonomy(soup: BeautifulSoup, kind: str) -> list[str]:
    result: list[str] = []
    metadata = soup.select_one("article.post-content .post-metas")
    if metadata is None:
        return result
    for anchor in metadata.select(f'a[href^="/{kind}/"]'):
        value = anchor.get_text(" ", strip=True)
        if value and value not in result:
            result.append(value)
    return result


def code_fence(code: str, language: str) -> str:
    longest = max((len(match) for match in re.findall(r"`+", code)), default=0)
    fence = "`" * max(3, longest + 1)
    return f"{fence}{language}\n{code.rstrip()}\n{fence}"


def prepare_content(container: Tag) -> tuple[str, int]:
    for anchor in container.select("a.headerlink"):
        anchor.decompose()

    for checkbox in container.select('input[type="checkbox"]'):
        checked = checkbox.has_attr("checked")
        checkbox.replace_with(NavigableString("[x] " if checked else "[ ] "))

    replacements: dict[str, str] = {}
    for index, figure in enumerate(container.select("figure.highlight")):
        code_node = figure.select_one("td.code pre code") or figure.select_one("pre code")
        if code_node is None:
            continue
        for br in code_node.find_all("br"):
            br.replace_with(NavigableString("\n"))
        code = code_node.get_text("", strip=False).replace("\u00a0", " ")
        classes = [str(item) for item in figure.get("class", []) if item != "highlight"]
        language = LANGUAGE_MAP.get(classes[0].lower(), classes[0].lower()) if classes else ""
        language = re.sub(r"[^a-z0-9_+#.-]", "", language)
        token = f"HEXORECOVEREDCODEBLOCK{index:06d}TOKEN"
        replacements[token] = code_fence(code, language)
        figure.replace_with(NavigableString(f"\n\n{token}\n\n"))

    result = markdownify(
        str(container),
        heading_style="ATX",
        bullets="-",
        strip=["script", "style"],
    )
    for token, block in replacements.items():
        result = result.replace(token, block)
    result = re.sub(r"\n{4,}", "\n\n\n", result).strip()
    return result + "\n", len(replacements)


def safe_filename(date: str, slug: str, used: set[str]) -> str:
    cleaned = re.sub(r'[\\/:*?"<>|\x00-\x1f]', "-", slug).strip(" .") or "untitled"
    stem = f"{date[:10]}-{cleaned}"
    candidate = f"{stem}.md"
    key = candidate.casefold()
    if key in used:
        digest = hashlib.sha1(slug.encode("utf-8")).hexdigest()[:8]
        candidate = f"{stem}-{digest}.md"
        key = candidate.casefold()
    used.add(key)
    return candidate


def write_markdown(path: Path, metadata: dict[str, object], body: str) -> None:
    front_matter = yaml.safe_dump(
        metadata,
        allow_unicode=True,
        sort_keys=False,
        default_flow_style=False,
        width=1000,
    ).rstrip()
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(f"---\n{front_matter}\n---\n\n{body}", encoding="utf-8")


def recover_posts(repo: Path, revision: str, output: Path) -> tuple[int, int, list[str]]:
    output.mkdir(parents=True, exist_ok=True)
    used: set[str] = set()
    failures: list[str] = []
    total_code_blocks = 0
    count = 0

    for path in git_paths(repo, revision):
        match = POST_PATH.match(path)
        if not match:
            continue
        year, month, day, slug = match.groups()
        soup = BeautifulSoup(git_text(repo, revision, path), "html.parser")
        content = soup.select_one("article.post-content .markdown-body")
        if content is None:
            failures.append(f"missing content: {path}")
            continue
        title = recover_title(soup, slug)
        date = recover_date(soup, year, month, day)
        body, code_blocks = prepare_content(content)
        metadata: dict[str, object] = {
            "title": title,
            "date": date,
            "permalink": path.removesuffix("index.html"),
        }
        categories = recover_taxonomy(soup, "categories")
        tags = recover_taxonomy(soup, "tags")
        if categories:
            metadata["categories"] = categories
        if tags:
            metadata["tags"] = tags
        filename = safe_filename(date, slug, used)
        write_markdown(output / filename, metadata, body)
        total_code_blocks += code_blocks
        count += 1

    return count, total_code_blocks, failures


def recover_about(repo: Path, revision: str, source_root: Path) -> bool:
    soup = BeautifulSoup(git_text(repo, revision, "about/index.html"), "html.parser")
    content = soup.select_one(".markdown-body") or soup.select_one(".page-content")
    if content is None:
        return False
    body, _ = prepare_content(content)
    write_markdown(
        source_root / "about" / "index.md",
        {"title": "关于", "date": "2021-06-06 00:00:00", "layout": "page", "permalink": "about/"},
        body,
    )
    return True


def recover_links(repo: Path, revision: str, source_root: Path) -> int:
    soup = BeautifulSoup(git_text(repo, revision, "links/index.html"), "html.parser")
    links: list[dict[str, str]] = []
    for card in soup.select(".links .card"):
        anchor = card.select_one("a[href]")
        title = text_or_none(card.select_one(".link-title"))
        if anchor is None or title is None:
            continue
        item = {"name": title, "link": str(anchor.get("href", ""))}
        avatar = card.select_one(".link-avatar img[src]")
        description = text_or_none(card.select_one(".link-intro"))
        if avatar is not None:
            item["avatar"] = str(avatar.get("src", ""))
        if description:
            item["descr"] = description
        links.append(item)
    data_path = source_root / "_data" / "links.yml"
    data_path.parent.mkdir(parents=True, exist_ok=True)
    data_path.write_text(
        yaml.safe_dump(links, allow_unicode=True, sort_keys=False, width=1000),
        encoding="utf-8",
    )
    return len(links)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo", type=Path, required=True)
    parser.add_argument("--revision", default="master")
    parser.add_argument("--source-root", type=Path, required=True)
    args = parser.parse_args()

    posts = args.source_root / "_posts"
    count, code_blocks, failures = recover_posts(args.repo, args.revision, posts)
    about = recover_about(args.repo, args.revision, args.source_root)
    links = recover_links(args.repo, args.revision, args.source_root)
    print(f"Recovered posts: {count}")
    print(f"Recovered code blocks: {code_blocks}")
    print(f"Recovered about page: {about}")
    print(f"Recovered links: {links}")
    for failure in failures:
        print(f"ERROR {failure}")
    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(main())
