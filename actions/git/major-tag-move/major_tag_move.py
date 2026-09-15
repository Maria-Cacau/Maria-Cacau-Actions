import subprocess
import sys


def git(*args: str) -> subprocess.CompletedProcess:
    return subprocess.run(["git", *args], capture_output=True, text=True, check=True)


def main() -> None:
    version = sys.argv[1]
    tag = f"v{version.split('.')[0]}"

    git("config", "user.name", "github-actions[bot]")
    git("config", "user.email", "github-actions[bot]@users.noreply.github.com")

    git("tag", "-fa", tag, "-m", f"{tag} — {version}")
    git("push", "-f", "origin", tag)
    print(f"Tag '{tag}' apontando para a versão {version}.")


if __name__ == "__main__":
    main()
