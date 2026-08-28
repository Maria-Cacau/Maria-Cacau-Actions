import os
import re
import subprocess
import sys

VERSION_RE = re.compile(r'version = "(\d+\.\d+\.\d+)"')


def read_version(ref: str) -> str | None:
    result = subprocess.run(
        ["git", "show", f"{ref}:pyproject.toml"],
        capture_output=True,
        text=True,
    )
    if result.returncode != 0:
        return None
    match = VERSION_RE.search(result.stdout)
    return match.group(1) if match else None


def main() -> None:
    current = read_version("HEAD")
    previous = read_version("HEAD^")

    if current is None:
        print(
            '::error title=check-version::não encontrei \'version = "x.y.z"\' em pyproject.toml',
            file=sys.stderr,
        )
        sys.exit(1)

    changed = current != previous
    print(f"Versão atual: {current} | anterior: {previous or '(nenhuma)'} | mudou: {changed}")

    github_output = os.environ.get("GITHUB_OUTPUT")
    if github_output:
        with open(github_output, "a", encoding="utf-8") as f:
            f.write(f"changed={'true' if changed else 'false'}\n")
            f.write(f"version={current}\n")


if __name__ == "__main__":
    main()
