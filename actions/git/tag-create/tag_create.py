import os
import subprocess
import sys


def gh(*args: str, check: bool = True) -> subprocess.CompletedProcess:
    return subprocess.run(["gh", *args], capture_output=True, text=True, check=check)


def git(*args: str, check: bool = True) -> subprocess.CompletedProcess:
    return subprocess.run(["git", *args], capture_output=True, text=True, check=check)


def main() -> None:
    tag = sys.argv[1]
    message = sys.argv[2] if len(sys.argv) > 2 else f"Tag {tag}"
    repo = os.environ["GITHUB_REPOSITORY"]

    # Tag anotada precisa de identidade configurada (tagger).
    git("config", "user.name", "github-actions[bot]")
    git("config", "user.email", "github-actions[bot]@users.noreply.github.com")

    # Apaga se já existir, pra "mover" a tag pro commit atual em vez de falhar.
    gh("api", "--method", "DELETE", f"repos/{repo}/git/refs/tags/{tag}", check=False)

    git("tag", "-a", tag, "-m", message)
    git("push", "origin", tag)
    print(f"Tag '{tag}' criada/atualizada, apontando pro commit atual.")


if __name__ == "__main__":
    main()
