import sys
from typing import Dict
from PyQt5.QtWidgets import (
    QApplication,
    QMainWindow,
    QTextEdit,
    QAction,
    QFileDialog,
    QMessageBox,
    QToolBar,
)
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt


class TextEditorMainWindow(QMainWindow):
    """Main window that provides the text editor user interface."""

    def __init__(self) -> None:
        super().__init__()
        self._file_path: str | None = None
        self._setup_ui()

    def _setup_ui(self) -> None:
        """Configure the main window, menus, toolbars and central widget."""
        self.setWindowTitle("PyQt Text Editor")
        self.resize(800, 600)

        # Central text editor
        self.text_edit = QTextEdit()
        self.setCentralWidget(self.text_edit)

        # Status bar
        self.statusBar().showMessage("Ready")

        # Create actions, menus and toolbars
        self._create_actions()
        self._create_menus()
        self._create_toolbars()

    def _create_actions(self) -> None:
        """Create actions used in menus and toolbars."""
        self.actions: Dict[str, QAction] = {}

        new_action = QAction(QIcon(), "New", self)
        new_action.setShortcut("Ctrl+N")
        new_action.setStatusTip("Create a new document")
        new_action.triggered.connect(self.on_new_file)
        self.actions["new"] = new_action

        open_action = QAction(QIcon(), "Open...", self)
        open_action.setShortcut("Ctrl+O")
        open_action.setStatusTip("Open an existing text file")
        open_action.triggered.connect(self.on_open_file)
        self.actions["open"] = open_action

        save_action = QAction(QIcon(), "Save", self)
        save_action.setShortcut("Ctrl+S")
        save_action.setStatusTip("Save the current document")
        save_action.triggered.connect(self.on_save_file)
        self.actions["save"] = save_action

        save_as_action = QAction(QIcon(), "Save As...", self)
        save_as_action.setStatusTip("Save the current document under a new name")
        save_as_action.triggered.connect(self.on_save_file_as)
        self.actions["save_as"] = save_as_action

        exit_action = QAction(QIcon(), "Exit", self)
        exit_action.setShortcut("Ctrl+Q")
        exit_action.setStatusTip("Exit the application")
        exit_action.triggered.connect(self.close)
        self.actions["exit"] = exit_action

        undo_action = QAction(QIcon(), "Undo", self)
        undo_action.setShortcut("Ctrl+Z")
        undo_action.setStatusTip("Undo last action")
        undo_action.triggered.connect(self.text_edit.undo)
        self.actions["undo"] = undo_action

        redo_action = QAction(QIcon(), "Redo", self)
        redo_action.setShortcut("Ctrl+Y")
        redo_action.setStatusTip("Redo last undone action")
        redo_action.triggered.connect(self.text_edit.redo)
        self.actions["redo"] = redo_action

        cut_action = QAction(QIcon(), "Cut", self)
        cut_action.setShortcut("Ctrl+X")
        cut_action.setStatusTip("Cut selection to clipboard")
        cut_action.triggered.connect(self.text_edit.cut)
        self.actions["cut"] = cut_action

        copy_action = QAction(QIcon(), "Copy", self)
        copy_action.setShortcut("Ctrl+C")
        copy_action.setStatusTip("Copy selection to clipboard")
        copy_action.triggered.connect(self.text_edit.copy)
        self.actions["copy"] = copy_action

        paste_action = QAction(QIcon(), "Paste", self)
        paste_action.setShortcut("Ctrl+V")
        paste_action.setStatusTip("Paste text from clipboard")
        paste_action.triggered.connect(self.text_edit.paste)
        self.actions["paste"] = paste_action

        about_action = QAction("About", self)
        about_action.setStatusTip("Show information about this application")
        about_action.triggered.connect(self.on_about)
        self.actions["about"] = about_action

    def _create_menus(self) -> None:
        """Create the main menu bar and its menus."""
        menu_bar = self.menuBar()

        file_menu = menu_bar.addMenu("&File")
        file_menu.addAction(self.actions["new"])
        file_menu.addAction(self.actions["open"])
        file_menu.addAction(self.actions["save"])
        file_menu.addAction(self.actions["save_as"])
        file_menu.addSeparator()
        file_menu.addAction(self.actions["exit"])

        edit_menu = menu_bar.addMenu("&Edit")
        edit_menu.addAction(self.actions["undo"])
        edit_menu.addAction(self.actions["redo"])
        edit_menu.addSeparator()
        edit_menu.addAction(self.actions["cut"])
        edit_menu.addAction(self.actions["copy"])
        edit_menu.addAction(self.actions["paste"])

        help_menu = menu_bar.addMenu("&Help")
        help_menu.addAction(self.actions["about"])

    def _create_toolbars(self) -> None:
        """Create toolbars with frequently used actions."""
        file_toolbar = QToolBar("File", self)
        file_toolbar.setIconSize(Qt.QSize(16, 16)) if hasattr(Qt, "QSize") else None
        self.addToolBar(file_toolbar)
        file_toolbar.addAction(self.actions["new"])
        file_toolbar.addAction(self.actions["open"])
        file_toolbar.addAction(self.actions["save"])

        edit_toolbar = QToolBar("Edit", self)
        self.addToolBar(edit_toolbar)
        edit_toolbar.addAction(self.actions["undo"])
        edit_toolbar.addAction(self.actions["redo"])
        edit_toolbar.addSeparator()
        edit_toolbar.addAction(self.actions["cut"])
        edit_toolbar.addAction(self.actions["copy"])
        edit_toolbar.addAction(self.actions["paste"])

    def on_new_file(self) -> None:
        """Clear the editor and reset file path."""
        self._file_path = None
        self.text_edit.clear()
        self.statusBar().showMessage("New document", 2000)

    def on_open_file(self) -> None:
        """Open a text file from disk and load its contents."""
        path, _ = QFileDialog.getOpenFileName(
            self,
            "Open File",
            "",
            "Text Files (*.txt);;All Files (*)",
        )
        if not path:
            return
        try:
            with open(path, "r", encoding="utf-8") as file:
                content = file.read()
        except OSError as error:
            QMessageBox.critical(self, "Open File", f"Could not open file:\n{error}")
            return
        self._file_path = path
        self.text_edit.setPlainText(content)
        self.statusBar().showMessage(f"Opened: {path}", 2000)
        self.setWindowTitle(f"PyQt Text Editor - {path}")

    def on_save_file(self) -> None:
        """Save the current document to disk."""
        if self._file_path is None:
            self.on_save_file_as()
            return
        self._write_to_path(self._file_path)

    def on_save_file_as(self) -> None:
        """Ask for a file path and save the current document."""
        path, _ = QFileDialog.getSaveFileName(
            self,
            "Save File As",
            "",
            "Text Files (*.txt);;All Files (*)",
        )
        if not path:
            return
        self._write_to_path(path)
        self._file_path = path
        self.setWindowTitle(f"PyQt Text Editor - {path}")

    def _write_to_path(self, path: str) -> None:
        """Write editor contents to the given file path."""
        try:
            content = self.text_edit.toPlainText()
            with open(path, "w", encoding="utf-8") as file:
                file.write(content)
        except OSError as error:
            QMessageBox.critical(self, "Save File", f"Could not save file:\n{error}")
            return
        self.statusBar().showMessage(f"Saved: {path}", 2000)

    def on_about(self) -> None:
        """Show simple About dialog."""
        QMessageBox.information(
            self,
            "About",
            "PyQt Text Editor\n\nSimple example of menus, toolbars and status bar.",
        )


def main() -> None:
    """Entry point of the text editor application."""
    app = QApplication(sys.argv)
    window = TextEditorMainWindow()
    window.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
