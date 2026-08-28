import json
import os
import re
import subprocess
import sys
from pathlib import Path

VERSION_RE = re.compile(r'version = "(\d+)\.(\d+)\.(\d+)"')
TAG_RE = re.compile(r"v?(\d+)\.(\d+)\.(\d+)")


def current_version() -> tuple[int, int, int]:
    text = Path("pyproject.toml").read_text(encoding="utf-8")
    match = VERSION_RE.search(text)
    if not match:
        print(
            '::error title=check-version::não encontrei \'version = "x.y.z"\' em pyproject.toml',
            file=sys.stderr,
        )
        sys.exit(1)
    return tuple(int(g) for g in match.groups())


def latest_released_version() -> tuple[int, int, int] | None:
    result = subprocess.run(
        ["gh", "release", "list", "--json", "tagName", "--limit", "100"],
        capture_output=True,
        text=True,
    )
    if result.returncode != 0:
        return None
    versions = []
    for release in json.loads(result.stdout):
        match = TAG_RE.fullmatch(release["tagName"])
        if match:
            versions.append(tuple(int(g) for g in match.groups()))
    return max(versions) if versions else None


def main() -> None:
    current = current_version()
    current_str = ".".join(map(str, current))
    latest = latest_released_version()

    changed = latest is None or current > latest

    if changed:
        latest_str = ".".join(map(str, latest)) if latest else "(nenhuma)"
        print(f"Versão atual: {current_str} | última release: {latest_str} | segue")
    else:
        latest_str = ".".join(map(str, latest))
        print(
            f"::warning title=check-version::Não foi identificado a troca de versão; "
            f"tag {latest_str} já existe."
        )

    github_output = os.environ.get("GITHUB_OUTPUT")
    if github_output:
        with open(github_output, "a", encoding="utf-8") as f:
            f.write(f"changed={'true' if changed else 'false'}\n")
            f.write(f"version={current_str}\n")


if __name__ == "__main__":
    main()
