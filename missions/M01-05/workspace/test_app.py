from app import format_status


def main() -> None:
    assert format_status("nvim") == "nvim: READY!"
    assert format_status("tmux") == "tmux: READY!"
    print("ok")


if __name__ == "__main__":
    main()
