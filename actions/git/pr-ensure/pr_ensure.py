import json
import subprocess
import sys


def gh(*args: str, check: bool = True) -> subprocess.CompletedProcess:
    return subprocess.run(["gh", *args], capture_output=True, text=True, check=check)


def main() -> None:
    target = sys.argv[1]
    branch = sys.argv[2]
    title = sys.argv[3]

    pr_view = gh("pr", "view", branch, "--json", "state", check=False)
    if pr_view.returncode != 0:
        print(f"Criando PR de {branch} para {target}...")
        gh("pr", "create", "--base", target, "--head", branch, "--title", title, "--body", "")
        return

    state = json.loads(pr_view.stdout)["state"]
    if state == "OPEN":
        print(f"PR para {branch} já existe e está aberto, pulando criação.")
    elif state == "CLOSED":
        print(f"PR para {branch} existe mas está fechado. Reabrindo...")
        gh("pr", "reopen", branch)
    elif state == "MERGED":
        print(f"AVISO: PR para {branch} já foi mergeado anteriormente. Nada a fazer.")


if __name__ == "__main__":
    main()
