import os
import subprocess
import sys


def main() -> None:
    target = sys.argv[1] if len(sys.argv) > 1 else "."

    check = subprocess.run(
        [sys.executable, "-m", "isort", "--check-only", target],
        capture_output=True,
        text=True,
    )
    changed = check.returncode != 0

    if changed:
        subprocess.run([sys.executable, "-m", "isort", target], check=True)
        print(f"isort ajustou imports em: {target}")
    else:
        print("Nenhum import fora de ordem.")

    github_output = os.environ.get("GITHUB_OUTPUT")
    if github_output:
        with open(github_output, "a", encoding="utf-8") as f:
            f.write(f"changed={'true' if changed else 'false'}\n")


if __name__ == "__main__":
    main()
