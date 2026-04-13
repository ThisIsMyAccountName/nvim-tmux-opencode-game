from src.a import FLAG_DISABLED, value
from src.b import is_off
from src.c import label


def main() -> None:
    assert FLAG_DISABLED == "off"
    assert value() == "off"
    assert is_off() is True
    assert label() == "state:off"
    print("ok")


if __name__ == "__main__":
    main()
