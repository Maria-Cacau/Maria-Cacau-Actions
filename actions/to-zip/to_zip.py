import os
import sys
import zipfile
from pathlib import Path


def main() -> None:
    source = Path(sys.argv[1])
    if not source.is_file():
        print(f"::error title=to-zip::arquivo não encontrado: {source}", file=sys.stderr)
        sys.exit(1)

    target = source.with_suffix(".zip")
    with zipfile.ZipFile(target, "w", zipfile.ZIP_DEFLATED) as archive:
        archive.write(source, arcname=source.name)

    size = target.stat().st_size / 1048576
    print(f"{source.name} compactado em {target.name} ({size:.1f} MB).")

    github_output = os.environ.get("GITHUB_OUTPUT")
    if github_output:
        with open(github_output, "a", encoding="utf-8") as f:
            f.write(f"zip-path={target}\n")


if __name__ == "__main__":
    main()
