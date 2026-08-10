#!/usr/bin/env python3
"""Build the Christian-source registry and optionally check URL metadata."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import urllib.error
import urllib.request
from datetime import UTC, datetime, timedelta
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
GUIDE = ROOT / "tools" / "christian_traditions_sources.md"
REGISTRY = ROOT / "tools" / "christian_sources.json"
CACHE = ROOT / ".tmp" / "christian_source_status.json"
URL_RE = re.compile(r"https?://[^\s)>]+")
PERMANENT_FAILURES = {404, 410}


def extract_sources(guide: Path = GUIDE) -> list[dict[str, str]]:
    section = ""
    sources: list[dict[str, str]] = []
    seen: set[str] = set()
    for line in guide.read_text(encoding="utf-8-sig").splitlines():
        if line.startswith("## "):
            section = line[3:].strip()
        for raw_url in URL_RE.findall(line):
            url = raw_url.rstrip(".,")
            if url in seen:
                continue
            seen.add(url)
            sources.append(
                {
                    "id": hashlib.sha256(url.encode("utf-8")).hexdigest()[:12],
                    "section": section,
                    "url": url,
                    "use": "人工核对词目；不抓取或再分发释义与正文",
                }
            )
    return sources


def render_registry(root: Path = ROOT) -> str:
    guide = root / "tools" / "christian_traditions_sources.md"
    payload = {
        "schema_version": 1,
        "generated_from": "tools/christian_traditions_sources.md",
        "guide_sha256": hashlib.sha256(guide.read_bytes()).hexdigest(),
        "sources": extract_sources(guide),
    }
    return json.dumps(payload, ensure_ascii=False, indent=2) + "\n"


def load_cache(path: Path) -> dict[str, dict[str, object]]:
    if not path.is_file():
        return {}
    payload = json.loads(path.read_text(encoding="utf-8"))
    return payload.get("sources", {}) if isinstance(payload, dict) else {}


def check_online(
    sources: list[dict[str, str]], cache_path: Path = CACHE, max_age_days: int = 7
) -> tuple[dict[str, dict[str, object]], list[str]]:
    cache = load_cache(cache_path)
    now = datetime.now(UTC)
    failures: list[str] = []
    for source in sources:
        url = source["url"]
        previous = cache.get(url, {})
        checked_at = previous.get("checked_at")
        if isinstance(checked_at, str):
            try:
                checked = datetime.fromisoformat(checked_at)
            except ValueError:
                checked = None
            if checked and now - checked < timedelta(days=max_age_days):
                continue
        headers = {"User-Agent": "eosphoros-keytao-source-check/1.0"}
        if previous.get("etag"):
            headers["If-None-Match"] = str(previous["etag"])
        if previous.get("last_modified"):
            headers["If-Modified-Since"] = str(previous["last_modified"])
        status = 0
        response_headers: object = {}
        try:
            request = urllib.request.Request(url, headers=headers, method="HEAD")
            with urllib.request.urlopen(request, timeout=20) as response:
                status = response.status
                response_headers = response.headers
        except urllib.error.HTTPError as exc:
            status = exc.code
            response_headers = exc.headers
            if status in {403, 405}:
                try:
                    request = urllib.request.Request(
                        url, headers={**headers, "Range": "bytes=0-0"}, method="GET"
                    )
                    with urllib.request.urlopen(request, timeout=20) as response:
                        status = response.status
                        response_headers = response.headers
                except urllib.error.HTTPError as retry:
                    status = retry.code
                    response_headers = retry.headers
                except OSError:
                    status = 0
        except OSError:
            status = 0
        if status == 304:
            status = int(previous.get("status", 200))
        get_header = getattr(response_headers, "get", lambda _name: None)
        cache[url] = {
            "status": status,
            "checked_at": now.isoformat(),
            "etag": get_header("ETag") or previous.get("etag"),
            "last_modified": get_header("Last-Modified") or previous.get("last_modified"),
        }
        if status in PERMANENT_FAILURES:
            failures.append(f"{status} {url}")
    cache_path.parent.mkdir(parents=True, exist_ok=True)
    cache_path.write_text(
        json.dumps({"sources": cache}, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
        newline="\n",
    )
    return cache, failures


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--write", action="store_true")
    parser.add_argument("--check", action="store_true")
    parser.add_argument("--online", action="store_true")
    parser.add_argument("--cache", type=Path, default=CACHE)
    args = parser.parse_args()
    expected = render_registry()
    if args.write:
        REGISTRY.write_text(expected, encoding="utf-8", newline="\n")
    if args.check and (not REGISTRY.is_file() or REGISTRY.read_text(encoding="utf-8") != expected):
        print("Christian source registry is stale; run with --write.")
        return 1
    sources = json.loads(expected)["sources"]
    if args.online:
        cache, failures = check_online(sources, args.cache)
        counts: dict[int, int] = {}
        for item in cache.values():
            status = int(item.get("status", 0))
            counts[status] = counts.get(status, 0) + 1
        print("Source status:", ", ".join(f"{key}={value}" for key, value in sorted(counts.items())))
        if failures:
            print("Permanently unavailable sources:\n" + "\n".join(failures))
            return 2
    print(f"Christian source registry: {len(sources)} unique URLs")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
