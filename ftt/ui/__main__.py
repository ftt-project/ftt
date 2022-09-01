from PyQt6.QtWidgets import QApplication

from ftt.ui.application import Application


def main() -> None:
    window = Application([])
    window.run()


if __name__ == "__main__":
    main()
