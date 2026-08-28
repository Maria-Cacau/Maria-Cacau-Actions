import os
import sys


def main() -> None:
    expected = sys.argv[1] if len(sys.argv) > 1 else "main"
    current = os.environ.get("GITHUB_REF_NAME", "")

    if current != expected:
        print(
            f"::error title=check-branch::Branch atual é '{current}', mas release só pode "
            f"ser gerada a partir de '{expected}'.",
            file=sys.stderr,
        )
        sys.exit(1)

    print(f"Branch OK: {current}")


if __name__ == "__main__":
    main()
