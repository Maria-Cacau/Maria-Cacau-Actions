import os
import subprocess
import sys


def main() -> None:
    key = sys.argv[1]
    repo = os.environ["GITHUB_REPOSITORY"]

    result = subprocess.run(
        ["gh", "api", "--method", "DELETE", f"repos/{repo}/actions/caches?key={key}"],
        capture_output=True,
        text=True,
    )
    if result.returncode == 0:
        print(f"Cache '{key}' apagado.")
    else:
        print(f"Nenhum cache '{key}' encontrado (ou já removido) — seguindo.")


if __name__ == "__main__":
    main()
