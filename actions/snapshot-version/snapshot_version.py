import os
import re
import sys
from pathlib import Path

VERSION_RE = re.compile(r'version = "(\d+\.\d+\.\d+)"')


def main() -> None:
    match = VERSION_RE.search(Path("pyproject.toml").read_text(encoding="utf-8"))
    if not match:
        print(
            '::error title=snapshot-version::não encontrei \'version = "x.y.z"\' em pyproject.toml',
            file=sys.stderr,
        )
        sys.exit(1)

    version = match.group(1)
    # run_number é sequencial por workflow — a tag mais recente é a de maior número. O quarto número
    # segue o formato de versão de arquivo do Windows (M.m.p.b).
    tag = f"{version}.{os.environ['GITHUB_RUN_NUMBER']}-SNAPSHOT"
    print(f"Snapshot: {tag}")

    github_output = os.environ.get("GITHUB_OUTPUT")
    if github_output:
        with open(github_output, "a", encoding="utf-8") as f:
            f.write(f"version={version}\n")
            f.write(f"tag={tag}\n")


if __name__ == "__main__":
    main()
