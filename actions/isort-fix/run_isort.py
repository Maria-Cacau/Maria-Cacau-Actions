import os
import subprocess
import sys


def changed_files() -> list[str]:
    diff = subprocess.run(
        ["git", "diff", "--name-only"],
        capture_output=True,
        text=True,
        check=True,
    )
    return [line for line in diff.stdout.splitlines() if line]


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

    summary_path = os.environ.get("GITHUB_STEP_SUMMARY")
    if summary_path:
        with open(summary_path, "a", encoding="utf-8") as f:
            f.write("## isort\n\n")
            if changed:
                f.write(f"Realizado — **{n}** arquivo(s) alterado(s)\n\n")
                for file in files:
                    f.write(f"- `{file}`\n")
            else:
                f.write("Nenhum import fora de ordem.\n")


if __name__ == "__main__":
    main()
