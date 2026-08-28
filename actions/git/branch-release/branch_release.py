import os
import re
import subprocess
import sys
from pathlib import Path

VERSION_RE = re.compile(r'version = "(\d+)\.(\d+)\.(\d+)"')


def git(*args: str, check: bool = True) -> subprocess.CompletedProcess:
    return subprocess.run(["git", *args], capture_output=True, text=True, check=check)


def current_version() -> tuple[int, int, int]:
    text = Path("pyproject.toml").read_text(encoding="utf-8")
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
    text = Path("pyproject.toml").read_text(encoding="utf-8")
    new_text = VERSION_RE.sub(f'version = "{".".join(map(str, version))}"', text, count=1)
    Path("pyproject.toml").write_text(new_text, encoding="utf-8")


def remote_branch_exists(branch: str) -> bool:
    return git("ls-remote", "--exit-code", "--heads", "origin", branch, check=False).returncode == 0


def main() -> None:
    kind = sys.argv[1]

    current = current_version()
    new_version = bump_version(current, kind)
    version_str = ".".join(map(str, new_version))
    branch = f"release/{version_str}"

    if remote_branch_exists(branch):
        print(f"Branch remota já existe, reaproveitando: {branch}")
        git("checkout", "-b", branch, f"origin/{branch}")
        created = False
    else:
        print(f"Criando branch: {branch}")
        git("checkout", "-b", branch)
        write_version(new_version)
        created = True

    github_output = os.environ.get("GITHUB_OUTPUT")
    if github_output:
        with open(github_output, "a", encoding="utf-8") as f:
            f.write(f"version={version_str}\n")
            f.write(f"branch={branch}\n")
            f.write(f"created={'true' if created else 'false'}\n")


if __name__ == "__main__":
    main()
