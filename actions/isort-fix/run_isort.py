import os
import subprocess
import sys


def changed_files() -> list[str]:
    # --porcelain pega modificados E não-rastreados, ao contrário de `git diff` sozinho.
    status = subprocess.run(
        ["git", "status", "--porcelain"],
        capture_output=True,
        text=True,
        check=True,
    )
    return [line[3:] for line in status.stdout.splitlines() if line]


def summary_row(changed: bool, files: list[str]) -> str:
    """Linha de tabela pro summary combinado (isort + graphify), montado num step
    agregador do code-standardize.yml. Não escreve em lugar nenhum — só formata."""
    if not changed:
        return "| isort | Nenhum import fora de ordem | - |"
    return f"| isort | {len(files)} arquivo(s) alterado(s) | {', '.join(f'`{f}`' for f in files)} |"


def main() -> None:
    target = sys.argv[1] if len(sys.argv) > 1 else "."

    subprocess.run([sys.executable, "-m", "isort", target], check=True)

    files = changed_files()
    n = len(files)
    changed = n > 0

    if changed:
        print(f"isort ajustou {n} arquivo(s) em: {target}")
        for f in files:
            print(f"  - {f}")
        print(f"::notice title=isort::{n} arquivo(s) alterado(s)")
    else:
        print("Nenhum import fora de ordem.")

    github_output = os.environ.get("GITHUB_OUTPUT")
    if github_output:
        with open(github_output, "a", encoding="utf-8") as f:
            f.write(f"changed={'true' if changed else 'false'}\n")
            f.write(f"count={n}\n")


if __name__ == "__main__":
    main()
