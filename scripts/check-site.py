#!/usr/bin/env python3
"""Check deployable pages, local assets, font URLs, and the custom domain."""

from html.parser import HTMLParser
from pathlib import Path
import re
import sys
from urllib.parse import unquote, urlsplit


ROOT = Path(__file__).resolve().parents[1] / "public"
ORIGIN = "https://bonitasfoundation.org"
errors = []


def check_url(value, source):
    url = urlsplit(value)
    if url.scheme or url.netloc:
        if url.netloc != urlsplit(ORIGIN).netloc:
            return
    if not url.path:
        return
    target = ROOT / unquote(url.path.lstrip("/")) if url.path.startswith("/") else source.parent / unquote(url.path)
    if target.is_dir():
        target /= "index.html"
    if not target.is_file():
        errors.append(f"{source.relative_to(ROOT)}: missing local target {value}")


class Page(HTMLParser):
    def __init__(self):
        super().__init__()
        self.headings = 0
        self.current_links = 0
        self.canonical = None
        self.title = False
        self.references = []

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        self.headings += tag == "h1"
        self.current_links += attrs.get("aria-current") == "page"
        if tag == "title":
            self.title = True
        if tag == "link" and attrs.get("rel") == "canonical":
            self.canonical = attrs.get("href")
        if tag == "img" and not attrs.get("alt"):
            errors.append("Image has no descriptive alt text")
        for attr in ("href", "src"):
            if attrs.get(attr):
                self.references.append(attrs[attr])
        if attrs.get("srcset"):
            self.references.extend(item.strip().split()[0] for item in attrs["srcset"].split(","))


for relative in ("index.html", "about/index.html", "404.html"):
    source = ROOT / relative
    if not source.is_file():
        errors.append(f"Missing page: {relative}")
        continue
    page = Page()
    page.feed(source.read_text())
    if page.headings != 1:
        errors.append(f"{relative}: expected one h1, found {page.headings}")
    if not page.title:
        errors.append(f"{relative}: missing title")
    if relative != "404.html" and page.current_links != 1:
        errors.append(f"{relative}: navigation must identify the current page")
    if not page.canonical or not page.canonical.startswith(ORIGIN + "/"):
        errors.append(f"{relative}: incorrect canonical URL")
    for reference in page.references:
        check_url(reference, source)

for source in ROOT.rglob("*.css"):
    for reference in re.findall(r"url\([\"']?([^\"')]+)[\"']?\)", source.read_text()):
        check_url(reference, source)

if not (ROOT / "CNAME").is_file() or (ROOT / "CNAME").read_text().strip() != "bonitasfoundation.org":
    errors.append("CNAME must contain bonitasfoundation.org")
for required in (".nojekyll", "robots.txt", "sitemap.xml", "favicon.svg"):
    if not (ROOT / required).is_file():
        errors.append(f"Missing deployment file: {required}")
for font in ("regular", "bold", "italic"):
    source = ROOT / "fonts" / f"calendas-plus-{font}.woff2"
    if not source.is_file() or source.read_bytes()[:4] != b"wOF2":
        errors.append(f"Missing or invalid Calendas Plus {font} font")

if errors:
    print("\n".join(errors), file=sys.stderr)
    sys.exit(1)
print("Site checks passed: pages, navigation, assets, fonts, metadata and custom domain.")
