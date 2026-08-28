import importlib
import os
import subprocess
import sys
import tomllib
from pathlib import Path

REQUIRED_ATTRS = [
    "__app_name__",
    "__version__",
    "__icon_win__",
    "__company__",
    "__description__",
    "__copyright__",
]


def entry_module_name(pyproject: Path) -> str:
    data = tomllib.loads(pyproject.read_text(encoding="utf-8"))
    return data["project"]["name"].replace("-", "_")


def check_required_attrs(module) -> None:
    missing = [attr for attr in REQUIRED_ATTRS if not hasattr(module, attr)]
    if missing:
        print(
            f"::error title=distribute::atributos faltando em {module.__name__}: "
            f"{', '.join(missing)}. Todo módulo que usa a action 'distribute' precisa expor: "
            f"{', '.join(REQUIRED_ATTRS)}.",
            file=sys.stderr,
        )
        sys.exit(1)


def main() -> None:
    root = Path(sys.argv[1] if len(sys.argv) > 1 else ".").resolve()
    entry = entry_module_name(root / "pyproject.toml")

    print(f"Instalando dependências de build ({root / 'pyproject.toml'})...")
    subprocess.run(
        [sys.executable, "-m", "pip", "install", "-e", ".[build]"],
        cwd=root,
        check=True,
    )

    # pip install roda em subprocess separado — o processo atual não enxerga o
    # pacote recém-instalado sem isso, mesmo sendo o mesmo interpretador.
    sys.path.insert(0, str(root))

    print(f"Importando módulo de entrada: {entry}")
    module = importlib.import_module(entry)
    check_required_attrs(module)

    app_name = module.__app_name__
    win_version = f"{module.__version__}.0"
    output_dir = root / "dist"

    print(f"Gerando .exe via Nuitka ({app_name} {module.__version__})...")
    cmd = [
        sys.executable,
        "-m",
        "nuitka",
        "--onefile",
        "--enable-plugin=pyqt6",
        "--windows-console-mode=disable",
        f"--windows-icon-from-ico={module.__icon_win__}",
        f"--windows-product-name={app_name}",
        f"--windows-product-version={win_version}",
        f"--windows-file-version={win_version}",
        f"--windows-company-name={module.__company__}",
        f"--windows-file-description={module.__description__}",
        f"--copyright={module.__copyright__}",
        f"--include-data-dir={entry}/assets={entry}/assets",
        "--include-data-files=pyproject.toml=pyproject.toml",
        f"--output-filename={app_name}",
        f"--output-dir={output_dir}",
        entry,
    ]
    subprocess.run(cmd, cwd=root, check=True)

    exe_path = output_dir / f"{app_name}.exe"
    print(f"Gerado em: {exe_path}")

    github_output = os.environ.get("GITHUB_OUTPUT")
    if github_output:
        with open(github_output, "a", encoding="utf-8") as f:
            f.write(f"app-name={app_name}\n")
            f.write(f"exe-path={exe_path}\n")


if __name__ == "__main__":
    main()
