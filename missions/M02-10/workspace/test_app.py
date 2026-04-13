from app import run
from config import MODE


def main() -> None:
    assert MODE == "prod"
    assert run("nvim") == "nvim: READY!"
    assert run("tmux") == "tmux: READY!"
    print("ok")


if __name__ == "__main__":
    main()
