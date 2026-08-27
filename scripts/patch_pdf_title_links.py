#!/usr/bin/env python3
"""Replace the legacy title-page link row without repaginating the paper."""

from __future__ import annotations

import argparse
from pathlib import Path

import fitz


GITHUB_URL = "https://github.com/Xpounder-com/llms-in-modern-agentic-systems"
PROJECT_URL = "https://xpounder-com.github.io/llms-in-modern-agentic-systems/"

# PyMuPDF coordinates use a top-left origin. This band contains only the
# title-page links in both the pdfLaTeX base and the verified LuaLaTeX proof.
LINK_ROW = fitz.Rect(160, 196, 435, 214)
GITHUB_LINK = fitz.Rect(168.38, 196.58, 335.39, 212.52)
PROJECT_LINK = fitz.Rect(356.31, 196.58, 426.90, 212.52)


def patch_pdf(base_path: Path, proof_path: Path, output_path: Path) -> None:
    base = fitz.open(base_path)
    proof = fitz.open(proof_path)

    if base.page_count < 1 or proof.page_count < 1:
        raise ValueError("Both PDFs must contain at least one page")

    page = base[0]
    proof_page = proof[0]

    for link in page.get_links():
        if fitz.Rect(link["from"]).intersects(LINK_ROW):
            page.delete_link(link)

    # Remove the legacy text objects as well as their visible marks, then
    # transplant the verified vector row.
    page.add_redact_annot(LINK_ROW, fill=(1, 1, 1))
    page.apply_redactions()
    page.show_pdf_page(LINK_ROW, proof, proof_page.number, clip=LINK_ROW, overlay=True)

    page.insert_link({"kind": fitz.LINK_URI, "from": GITHUB_LINK, "uri": GITHUB_URL})
    page.insert_link({"kind": fitz.LINK_URI, "from": PROJECT_LINK, "uri": PROJECT_URL})

    output_path.parent.mkdir(parents=True, exist_ok=True)
    base.save(output_path, garbage=4, deflate=True, clean=True)
    proof.close()
    base.close()


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("base", type=Path, help="104-page pdfLaTeX paper to preserve")
    parser.add_argument("proof", type=Path, help="compiled proof containing the new link row")
    parser.add_argument("output", type=Path, help="patched PDF output")
    args = parser.parse_args()
    patch_pdf(args.base, args.proof, args.output)


if __name__ == "__main__":
    main()
