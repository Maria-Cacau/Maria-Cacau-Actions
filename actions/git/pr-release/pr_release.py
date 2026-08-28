import json
import os
import re
import subprocess
import sys
from pathlib import Path

VERSION_RE = re.compile(r'version = "(\d+)\.(\d+)\.(\d+)"')
COMMIT_SCRIPT = Path(__file__).resolve().parents[1] / "commit-bot" / "commit_bot.sh"


def gh(*args: str, check: bool = True) -> subprocess.CompletedProcess:
    return subprocess.run(["gh", *args], capture_output=True, text=True, check=check)


def git(*args: str, check: bool = True) -> subprocess.CompletedProcess:
    return subprocess.run(["git", *args], capture_output=True, text=True, check=check)


def current_version() -> tuple[int, int, int]:
    text = open("pyproject.toml", encoding="utf-8").read()
    match = VERSION_RE.search(text)
    if not match:
        sys.exit('ERRO: não encontrei \'version = "x.y.z"\' em pyproject.toml')
    return tuple(int(g) for g in match.groups())


def bump_version(version: tuple[int, int, int], kind: str) -> tuple[int, int, int]:
    major, minor, patch = version
    if kind == "major":
        return (major + 1, 0, 0)
    if kind == "minor":
        return (major, minor + 1, 0)
    if kind == "patch":
        return (major, minor, patch + 1)
    sys.exit(f"ERRO: bump inválido: {kind} (use major, minor ou patch)")


def write_version(version: tuple[int, int, int]) -> None:
    text = open("pyproject.toml", encoding="utf-8").read()
    new_text = VERSION_RE.sub(f'version = "{".".join(map(str, version))}"', text, count=1)
    open("pyproject.toml", "w", encoding="utf-8").write(new_text)


def remote_branch_exists(branch: str) -> bool:
    return git("ls-remote", "--exit-code", "--heads", "origin", branch, check=False).returncode == 0


def ensure_branch(branch: str, version: tuple[int, int, int], version_str: str) -> None:
    if remote_branch_exists(branch):
        print(f"Branch remota já existe, reaproveitando: {branch}")
        git("checkout", "-b", branch, f"origin/{branch}")
        return

    print(f"Criando branch: {branch}")
    git("checkout", "-b", branch)
    write_version(version)
    env = {**os.environ, "COMMIT_MESSAGE": f"chore: bump version to {version_str}"}
    subprocess.run(["bash", str(COMMIT_SCRIPT)], env=env, check=True)


def ensure_pr(branch: str, version_str: str) -> None:
    pr_view = gh("pr", "view", branch, "--json", "state", check=False)
    if pr_view.returncode != 0:
        print(f"Criando PR de {branch} para main...")
        gh("pr", "create", "--base", "main", "--head", branch, "--title", f"Release {version_str}", "--body", "")
        return

    state = json.loads(pr_view.stdout)["state"]
    if state == "OPEN":
        print(f"PR para {branch} já existe e está aberto, pulando criação.")
    elif state == "CLOSED":
        print(f"PR para {branch} existe mas está fechado. Reabrindo...")
        gh("pr", "reopen", branch)
    elif state == "MERGED":
        print(f"AVISO: PR para {branch} já foi mergeado anteriormente. Nada a fazer.")


def main() -> None:
    kind = sys.argv[1]

    current = current_version()
    new_version = bump_version(current, kind)
    version_str = ".".join(map(str, new_version))
    branch = f"release/{version_str}"

    ensure_branch(branch, new_version, version_str)
    ensure_pr(branch, version_str)

    print(f"Release {version_str} preparada. Branch: {branch}")

    github_output = os.environ.get("GITHUB_OUTPUT")
    if github_output:
        with open(github_output, "a", encoding="utf-8") as f:
            f.write(f"version={version_str}\n")
            f.write(f"branch={branch}\n")


if __name__ == "__main__":
    main()
