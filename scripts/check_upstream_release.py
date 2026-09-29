#!/usr/bin/env python3
"""Check the vendored gist release against Semantic Arts' published releases.

Two things can go wrong with ``upstream/gist<version>_webDownload/`` without
any change in this repository:

- Semantic Arts publishes a newer gist release, so the schema falls behind;
- the vendored files drift from the release they claim to be.

This script asks the GitHub API for the latest release of semanticarts/gist,
downloads the web-download zip of the vendored version, and compares every
vendored file with its copy in the zip, byte for byte. It prints a Markdown
report and exits 1 when a newer release exists or a file differs.

Set ``GITHUB_TOKEN`` to raise the API rate limit. Usage::

    python scripts/check_upstream_release.py [--report FILE]
"""
from __future__ import annotations

import argparse
import io
import json
import os
import re
import sys
import urllib.request
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
API = "https://api.github.com/repos/semanticarts/gist/releases"
VENDORED = re.compile(r"^gist(\d+\.\d+\.\d+)_webDownload$")


def _get(url: str, accept: str = "application/vnd.github+json") -> bytes:
    req = urllib.request.Request(url, headers={"Accept": accept, "User-Agent": "lmodel-gist-upstream-check"})
    token = os.environ.get("GITHUB_TOKEN")
    if token and url.startswith("https://api.github.com/"):
        req.add_header("Authorization", f"Bearer {token}")
    with urllib.request.urlopen(req, timeout=60) as resp:
        return resp.read()


def _version_key(v: str) -> tuple[int, ...]:
    """Numeric parts of a version, so a tag such as ``v14.2.0-beta`` still orders."""
    return tuple(int(x) for x in re.findall(r"\d+", v))


def check() -> tuple[list[str], bool]:
    """Return the report lines and whether anything needs attention."""
    dirs = [d for d in (ROOT / "upstream").iterdir() if d.is_dir() and VENDORED.match(d.name)]
    if len(dirs) != 1:
        return [f"- Expected one `upstream/gist<version>_webDownload/`, found {len(dirs)}."], True
    vendored_dir = dirs[0]
    vendored = VENDORED.match(vendored_dir.name).group(1)
    report = [f"- Vendored release: gist {vendored} (`upstream/{vendored_dir.name}/`)."]
    attention = False

    latest = json.loads(_get(f"{API}/latest"))["tag_name"].removeprefix("v")
    if _version_key(latest) > _version_key(vendored):
        attention = True
        report.append(
            f"- **Semantic Arts has published gist {latest}.** Replace `upstream/` with its web download "
            f"(https://github.com/semanticarts/gist/releases/tag/v{latest}), update the converter's "
            f"default path and `--version`, and run `just gen-project`."
        )
    else:
        report.append(f"- Latest published release: gist {latest}, the vendored one.")

    release = json.loads(_get(f"{API}/tags/v{vendored}"))
    asset = next((a for a in release.get("assets", []) if a["name"] == f"{vendored_dir.name}.zip"), None)
    if asset is None:
        return report + [f"- The v{vendored} release has no `{vendored_dir.name}.zip` asset to compare with."], True
    archive = zipfile.ZipFile(io.BytesIO(_get(asset["browser_download_url"], accept="application/octet-stream")))
    members = set(archive.namelist())

    differing = []
    files = sorted(p for p in vendored_dir.rglob("*") if p.is_file())
    for path in files:
        member = f"{vendored_dir.name}/{path.relative_to(vendored_dir).as_posix()}"
        if member not in members:
            differing.append(f"`{member}` is not in the release zip")
        elif archive.read(member) != path.read_bytes():
            differing.append(f"`{member}` differs from the release zip")
    if differing:
        attention = True
        report.append(f"- **{len(differing)} vendored file(s) differ from the v{vendored} release:**")
        report += [f"  - {d}" for d in differing]
    else:
        report.append(f"- All {len(files)} vendored files match the v{vendored} release zip byte for byte.")
    return report, attention


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--report", type=Path, help="Also write the Markdown report to this file")
    args = parser.parse_args(argv)
    lines, attention = check()
    text = "\n".join(lines) + "\n"
    print(text, end="")
    if args.report:
        args.report.write_text(text, encoding="utf-8")
    return 1 if attention else 0


if __name__ == "__main__":
    sys.exit(main())
