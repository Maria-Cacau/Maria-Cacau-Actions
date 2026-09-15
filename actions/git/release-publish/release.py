import json
import os
import subprocess
import sys


def gh(*args: str, check: bool = True) -> subprocess.CompletedProcess:
    return subprocess.run(["gh", *args], capture_output=True, text=True, check=check)


def release_exists(version: str) -> bool:
    return gh("release", "view", version, check=False).returncode == 0


def create_release(version: str, *, draft: bool, prerelease: bool, target: str, notes: str) -> None:
    args = ["release", "create", version, "--title", f"v{version}", "--notes", notes]
    if draft:
        args.append("--draft")
    if prerelease:
        args.append("--prerelease")
    if target:
        args += ["--target", target]
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
    asset_path = sys.argv[2] if len(sys.argv) > 2 else ""
    draft = sys.argv[3].lower() == "true" if len(sys.argv) > 3 else False
    prerelease = os.environ.get("RELEASE_PRERELEASE", "").lower() == "true"
    target = os.environ.get("RELEASE_TARGET", "")
    notes = os.environ.get("RELEASE_NOTES", "")

    if release_exists(version):
        print(f"Release v{version} já existe, reaproveitando...")
    else:
        kind = " (draft)" if draft else " (pre-release)" if prerelease else ""
        print(f"Release v{version} não encontrada. Criando{kind}...")
        create_release(version, draft=draft, prerelease=prerelease, target=target, notes=notes)

    # Notes informadas são a descrição definitiva — o corpo do PR só entra quando ninguém definiu uma.
    if not notes and not current_notes(version).strip():
        body = pr_body_for_current_commit()
        if body:
            gh("release", "edit", version, "--notes", body)
            print("Descrição da release preenchida com o corpo do PR mergeado.")
        else:
            print("Nenhum PR encontrado pra esse commit — notes ficam vazias.")

    if asset_path:
        print(f"Subindo {asset_path} na release v{version}...")
        gh("release", "upload", version, asset_path, "--clobber")
        print(f"Asset enviado para a release v{version}.")
    else:
        print("Nenhum asset informado — release sem arquivo anexado.")


if __name__ == "__main__":
    main()
