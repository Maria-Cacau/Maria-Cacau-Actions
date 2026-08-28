import re
import sys
from pathlib import Path

BADGE_RE = re.compile(r"(img\.shields\.io/badge/version-)[\d.]+(-orange)")
TAG_LINK_RE = re.compile(r"(releases/tag/)[\d.]+")


def main() -> None:
    version = sys.argv[1]
    readme = Path("README.md")

    if not readme.is_file():
        print("README.md não encontrado — nada a atualizar.")
        return

    text = readme.read_text(encoding="utf-8")
    new_text, n_badge = BADGE_RE.subn(rf"\g<1>{version}\g<2>", text)
    new_text, n_link = TAG_LINK_RE.subn(rf"\g<1>{version}", new_text)

    if n_badge == 0 and n_link == 0:
        print("::warning title=badge-update::Badge de versão não encontrado no README.md — nada a atualizar.")
        return

    readme.write_text(new_text, encoding="utf-8")
    print(f"README.md atualizado com a versão {version} ({n_badge} badge, {n_link} link de tag).")


if __name__ == "__main__":
    main()
