import os
import subprocess
import sys


def gh(*args: str, check: bool = True) -> subprocess.CompletedProcess:
    return subprocess.run(["gh", *args], capture_output=True, text=True, check=check)


def main() -> None:
    version = sys.argv[1]
    major, minor, *_ = version.split(".")
    test_tag = f"{major}.{minor}-Test"
    repo = os.environ["GITHUB_REPOSITORY"]

    result = gh("api", "--method", "DELETE", f"repos/{repo}/git/refs/tags/{test_tag}", check=False)
    if result.returncode == 0:
        print(f"Tag de teste '{test_tag}' removida.")
    else:
        print(f"Nenhuma tag de teste '{test_tag}' encontrada — nada a remover.")


if __name__ == "__main__":
    main()
