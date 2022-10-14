from .system_info import SystemInfo


def main() -> None:
    info = SystemInfo.from_current_system()
    info.print()


if __name__ == "__main__":
    main()
