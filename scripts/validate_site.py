#!/usr/bin/env python3
"""Run lightweight structural checks for the static project website."""

from __future__ import annotations

from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urlsplit


ROOT = Path(__file__).resolve().parents[1]
SITE_ROOTS = (ROOT / "docs", ROOT / "github-page", ROOT / "project-page")


class Document(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.ids: list[str] = []
        self.references: list[str] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        values = dict(attrs)
        if values.get("id"):
            self.ids.append(values["id"] or "")
        for name in ("href", "src"):
            if values.get(name):
                self.references.append(values[name] or "")


def parse(path: Path) -> Document:
    document = Document()
    document.feed(path.read_text(encoding="utf-8"))
    return document


def main() -> None:
    errors: list[str] = []
    documents = {
        path.resolve(): parse(path)
        for site_root in SITE_ROOTS
        for path in site_root.rglob("*.html")
    }

    for path, document in documents.items():
        duplicate_ids = sorted({item for item in document.ids if document.ids.count(item) > 1})
        for item in duplicate_ids:
            errors.append(f"{path.relative_to(ROOT)}: duplicate id #{item}")

        for raw in document.references:
            parsed = urlsplit(raw)
            if parsed.scheme or raw.startswith("//"):
                continue

            if parsed.path:
                target = (path.parent / unquote(parsed.path)).resolve()
                if parsed.path.endswith("/") or not Path(parsed.path).suffix:
                    target /= "index.html"
                if not target.exists():
                    errors.append(f"{path.relative_to(ROOT)}: missing local target {raw}")
                    continue
            else:
                target = path

            if parsed.fragment and target.suffix.lower() == ".html":
                target_document = documents.get(target) or (parse(target) if target.exists() else None)
                if target_document and parsed.fragment not in target_document.ids:
                    errors.append(f"{path.relative_to(ROOT)}: missing anchor {raw}")

    if errors:
        print("\n".join(errors))
        raise SystemExit(1)

    print(f"Validated {len(documents)} HTML pages: local files, anchors, and IDs are consistent.")


if __name__ == "__main__":
    main()
