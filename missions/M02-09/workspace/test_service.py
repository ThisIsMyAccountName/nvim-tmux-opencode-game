from pathlib import Path


def main() -> None:
    for path in Path("service").glob("*.py"):
        text = path.read_text(encoding="utf-8")
        assert "DEBUG_ME" not in text
    print("ok")


if __name__ == "__main__":
    main()
