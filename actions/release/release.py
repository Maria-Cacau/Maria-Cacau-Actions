import json
import os
import subprocess
import sys


def gh(*args: str, check: bool = True) -> subprocess.CompletedProcess:
    return subprocess.run(["gh", *args], capture_output=True, text=True, check=check)


def release_exists(version: str) -> bool:
    return gh("release", "view", version, check=False).returncode == 0


def create_release(version: str, *, draft: bool) -> None:
    args = ["release", "create", version, "--title", f"v{version}", "--notes", ""]
    if draft:
        args.append("--draft")
    gh(*args)


def pr_body_for_current_commit() -> str | None:
    sha = os.environ["GITHUB_SHA"]
    repo = os.environ["GITHUB_REPOSITORY"]
    result = gh("api", f"repos/{repo}/commits/{sha}/pulls", check=False)
    if result.returncode != 0:
        return None
    prs = json.loads(result.stdout)
    return prs[0]["body"] if prs else None


def current_notes(version: str) -> str:
    result = gh("release", "view", version, "--json", "body")
    return json.loads(result.stdout).get("body") or ""


def main() -> None:
    version = sys.argv[1]
    exe_path = sys.argv[2]
    draft = sys.argv[3].lower() == "true" if len(sys.argv) > 3 else False

    if release_exists(version):
        print(f"Release v{version} já existe, reaproveitando...")
    else:
        print(f"Release v{version} não encontrada. Criando{' (draft)' if draft else ''}...")
        create_release(version, draft=draft)

    if not current_notes(version).strip():
        body = pr_body_for_current_commit()
        if body:
            gh("release", "edit", version, "--notes", body)
            print("Descrição da release preenchida com o corpo do PR mergeado.")
        else:
            print("Nenhum PR encontrado pra esse commit — notes ficam vazias.")

    print(f"Subindo {exe_path} na release v{version}...")
    gh("release", "upload", version, exe_path, "--clobber")
    print(f"Asset enviado para a release v{version}.")


if __name__ == "__main__":
    main()
