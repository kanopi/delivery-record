#!/usr/bin/env python3
"""Build the GitHub Pages site for kanopi/delivery-record into site/.

The site's job is to make the canonical spec URI dereferenceable:

    https://kanopi.github.io/delivery-record/spec/v1

- spec/ is copied VERBATIM into site/spec/ so schema.json and every
  checks/*.json dereference at exactly their $id URLs, and the example
  records are fetchable as raw markdown.
- The repo's markdown entry points are rendered to HTML index pages on
  top of the verbatim copy (a directory URL serves the rendered page;
  the raw .md stays available alongside).

Requires: pip install markdown

Usage: python3 scripts/build-site.py   # writes ./site/
"""

from __future__ import annotations

import pathlib
import shutil

import markdown

ROOT = pathlib.Path(__file__).resolve().parent.parent
SITE = ROOT / "site"

# Rendered pages: source markdown -> (output dir under site/, href rewrites).
# Rewrites keep the few cross-document links working in rendered HTML while
# the verbatim .md copies keep working for raw consumers.
PAGES = {
    "README.md": (
        "",
        {
            "spec/v1/README.md": "spec/v1/",
            "spec/VERSIONING.md": "spec/versioning/",
            "MIGRATION.md": "migration/",
            "LICENSE.md": "license/",
            "CHANGELOG.md": "changelog/",
        },
    ),
    "MIGRATION.md": ("migration", {}),
    "LICENSE.md": ("license", {}),
    "CHANGELOG.md": ("changelog", {}),
    "spec/v1/README.md": ("spec/v1", {"../VERSIONING.md": "../versioning/"}),
    "spec/VERSIONING.md": ("spec/versioning", {"v1/README.md": "../v1/"}),
}

SHELL = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<style>
  body {{ max-width: 46rem; margin: 2rem auto; padding: 0 1rem;
         font: 16px/1.6 -apple-system, BlinkMacSystemFont, "Segoe UI",
         Roboto, sans-serif; color: #1f2328; }}
  pre {{ background: #f6f8fa; padding: 1rem; overflow-x: auto;
        border-radius: 6px; font-size: 85%; }}
  code {{ background: #f6f8fa; padding: .15em .35em; border-radius: 4px;
         font-size: 90%; }}
  pre code {{ background: none; padding: 0; }}
  table {{ border-collapse: collapse; display: block; overflow-x: auto; }}
  th, td {{ border: 1px solid #d1d9e0; padding: .4em .8em; }}
  th {{ background: #f6f8fa; }}
  a {{ color: #0969da; }}
  h1, h2, h3 {{ line-height: 1.25; }}
  blockquote {{ border-left: 4px solid #d1d9e0; margin-left: 0;
               padding-left: 1rem; color: #59636e; }}
  footer {{ margin-top: 3rem; padding-top: 1rem; border-top: 1px solid
           #d1d9e0; font-size: 85%; color: #59636e; }}
</style>
</head>
<body>
{body}
<footer>
  <a href="https://github.com/kanopi/delivery-record">kanopi/delivery-record</a>
  · MIT · Kanopi Studios
</footer>
</body>
</html>
"""


def first_heading(text: str) -> str:
    for line in text.splitlines():
        if line.startswith("# "):
            return line[2:].strip()
    return "Delivery Record"


def render(src: pathlib.Path, out_dir: pathlib.Path, rewrites: dict) -> None:
    text = src.read_text(encoding="utf-8")
    for old, new in rewrites.items():
        text = text.replace(f"]({old})", f"]({new})")
    body = markdown.markdown(text, extensions=["extra", "toc", "sane_lists"])
    out_dir.mkdir(parents=True, exist_ok=True)
    title = first_heading(text)
    if title != "Delivery Record":
        title += " · Delivery Record"
    (out_dir / "index.html").write_text(SHELL.format(title=title, body=body),
                                        encoding="utf-8")


def main() -> None:
    if SITE.exists():
        shutil.rmtree(SITE)
    SITE.mkdir()

    # 1. The spec, verbatim — this is what makes the $id URLs real.
    shutil.copytree(ROOT / "spec", SITE / "spec")

    # 2. Rendered pages on top.
    for rel, (out_rel, rewrites) in PAGES.items():
        render(ROOT / rel, SITE / out_rel if out_rel else SITE, rewrites)

    # 3. A tiny /spec/ landing so the directory URL isn't a 404.
    spec_index = "\n".join(
        [
            "# Delivery Record spec",
            "",
            "- [v1](v1/) — current version"
            " ([schema.json](v1/schema.json), [checks/](v1/checks/),"
            " [examples/](v1/examples/))",
            "- [Versioning policy](versioning/)",
        ]
    )
    body = markdown.markdown(spec_index, extensions=["extra"])
    (SITE / "spec" / "index.html").write_text(
        SHELL.format(title="Spec · Delivery Record", body=body),
        encoding="utf-8",
    )

    pages = sum(1 for _ in SITE.rglob("index.html"))
    files = sum(1 for p in SITE.rglob("*") if p.is_file())
    print(f"site/ built: {pages} rendered pages, {files} files total")


if __name__ == "__main__":
    main()
