import os
import subprocess
import sys
from pathlib import Path


def changed_files() -> list[str]:
    # --porcelain pega modificados E não-rastreados (ex: graphify-out/ na 1a execução,
    # que `git diff` sozinho não enxerga por não estar staged/tracked ainda).
    status = subprocess.run(
        ["git", "status", "--porcelain"],
        capture_output=True,
        text=True,
        check=True,
    )
    return [line[3:] for line in status.stdout.splitlines() if line]


def force_rebuild(path: Path) -> None:
    """Fallback quando `graphify update` recusa sobrescrever o grafo (guard-rail
    interno contra encolhimento silencioso). Não existe flag --force na CLI, só na
    API Python — ver Maria-Cacau-Study/demandas/ci-cd/decisoes/graphify-force.md."""
    import graphify.export as export

    original_to_json = export.to_json
    export.to_json = lambda *a, **kw: original_to_json(*a, **{**kw, "force": True})

    from graphify.watch import _rebuild_code

    ok = _rebuild_code(path)
    if not ok:
        print("::error title=graphify::fallback force também falhou", file=sys.stderr)
        sys.exit(1)


def summary_row(changed: bool, forced: bool, files: list[str]) -> str:
    """Linha de tabela pro summary combinado (isort + graphify), montado num step
    agregador do code-standardize.yml. Não escreve em lugar nenhum — só formata."""
    if not changed:
        return "| graphify | Grafo já atualizado | - |"
    detail = f"{len(files)} arquivo(s) alterado(s)" + (" (force)" if forced else "")
    return f"| graphify | {detail} | {', '.join(f'`{f}`' for f in files)} |"


def main() -> None:
    target = sys.argv[1] if len(sys.argv) > 1 else "."

    result = subprocess.run(
        [sys.executable, "-m", "graphify", "update", target],
        capture_output=True,
        text=True,
    )
    print(result.stdout)

    forced = False
    if result.returncode != 0:
        print(result.stderr, file=sys.stderr)
        print("::warning title=graphify::update recusado, acionando fallback force")
        forced = True
        force_rebuild(Path(target))

    files = changed_files()
    n = len(files)
    changed = n > 0

    if changed:
        label = f"{n} arquivo(s) alterado(s)" + (" (force)" if forced else "")
        print(f"graphify atualizou {label} em: {target}")
        for f in files:
            print(f"  - {f}")
    else:
        print("Grafo já atualizado.")

    github_output = os.environ.get("GITHUB_OUTPUT")
    if github_output:
        with open(github_output, "a", encoding="utf-8") as f:
            f.write(f"changed={'true' if changed else 'false'}\n")
            f.write(f"count={n}\n")
            f.write(f"forced={'true' if forced else 'false'}\n")


if __name__ == "__main__":
    main()
