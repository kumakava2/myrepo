#!/usr/bin/env python3
"""Simple website scraper.

Usage:
  python scrape_website.py https://example.com --selector "h1"
"""

from __future__ import annotations

import argparse
import sys
from typing import Iterable

import requests
from bs4 import BeautifulSoup


def scrape(url: str, selector: str, timeout: int = 15) -> Iterable[str]:
    """Fetch *url* and return stripped text for matching CSS *selector*."""
    headers = {
        "User-Agent": (
            "Mozilla/5.0 (compatible; SimpleScraper/1.0; "
            "+https://example.com/bot)"
        )
    }
    response = requests.get(url, headers=headers, timeout=timeout)
    response.raise_for_status()

    soup = BeautifulSoup(response.text, "html.parser")
    for element in soup.select(selector):
        text = element.get_text(" ", strip=True)
        if text:
            yield text


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Scrape text from a webpage using a CSS selector."
    )
    parser.add_argument("url", help="Target webpage URL")
    parser.add_argument(
        "--selector",
        default="title",
        help="CSS selector to extract text from (default: title)",
    )
    parser.add_argument(
        "--timeout", type=int, default=15, help="HTTP timeout in seconds"
    )
    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()

    try:
        results = list(scrape(args.url, args.selector, args.timeout))
    except requests.RequestException as exc:
        print(f"Request failed: {exc}", file=sys.stderr)
        return 1

    if not results:
        print("No matching content found.")
        return 0

    for idx, item in enumerate(results, start=1):
        print(f"{idx}. {item}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
