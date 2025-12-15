import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QTextEdit


class TextEditorMainWindow(QMainWindow):
    """Basic main window skeleton for the text editor."""

    def __init__(self) -> None:
        super().__init__()
        self._setup_ui()

    def _setup_ui(self) -> None:
        """Configure the main window and central editor widget."""
        self.setWindowTitle("PyQt Text Editor")
        self.resize(800, 600)

        # Create central text editor widget
        text_edit = QTextEdit()
        self.setCentralWidget(text_edit)


def main() -> None:
    """Entry point of the text editor application."""
    app = QApplication(sys.argv)
    window = TextEditorMainWindow()
    window.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
