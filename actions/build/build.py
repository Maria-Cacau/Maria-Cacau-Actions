import os
import platform
import subprocess
import sys
from pathlib import Path


def find_build_script(root: Path) -> Path | None:
    ext = "bat" if platform.system() == "Windows" else "sh"
    candidates = [root / f"build.{ext}", root / "scripts" / f"build.{ext}"]
    for candidate in candidates:
        if candidate.is_file():
            return candidate
    return None


def resolve_python(root: Path) -> str:
    """Se o script de build criou um venv próprio, os steps seguintes precisam
    usar o Python de dentro dele — a ativação do venv não sobrevive entre steps
    do Actions (cada `run:` é um processo novo)."""
    venv_python = (
        root / "venv" / "Scripts" / "python.exe"
        if platform.system() == "Windows"
        else root / "venv" / "bin" / "python"
    )
    return str(venv_python) if venv_python.is_file() else sys.executable


def main() -> None:
    root = Path(sys.argv[1] if len(sys.argv) > 1 else ".").resolve()
    args = sys.argv[2] if len(sys.argv) > 2 and sys.argv[2] else None

    script = find_build_script(root)
    if script is None:
        print(
            "::error title=build::não encontrei script de build (build.bat/build.sh na raiz "
            "do repo ou em scripts/) — o repo precisa ter um pra preparar o ambiente.",
            file=sys.stderr,
        )
        sys.exit(1)

    cmd = [str(script)] + ([args] if args else [])
    print(f"Rodando script de build: {script.relative_to(root)}" + (f" {args}" if args else ""))
    subprocess.run(cmd, cwd=root, check=True)

    python_path = resolve_python(root)
    print(f"Python a usar nos próximos steps: {python_path}")

    github_output = os.environ.get("GITHUB_OUTPUT")
    if github_output:
        with open(github_output, "a", encoding="utf-8") as f:
            f.write(f"python={python_path}\n")


if __name__ == "__main__":
    main()
