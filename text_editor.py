import sys
from typing import Dict, Optional
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


class TextDocumentModel:
    """Model that manages the current text document and file path."""

    def __init__(self) -> None:
        self._file_path: Optional[str] = None
        self._content: str = ""

    @property
    def file_path(self) -> Optional[str]:
        """Return current document path."""
        return self._file_path

    @file_path.setter
    def file_path(self, value: Optional[str]) -> None:
        """Set current document path."""
        self._file_path = value

    @property
    def content(self) -> str:
        """Return current document content."""
        return self._content

    @content.setter
    def content(self, value: str) -> None:
        """Set current document content."""
        self._content = value

    def load_from_disk(self, path: str) -> str:
        """Load text content from disk and update model state."""
        with open(path, "r", encoding="utf-8") as file:
            self._content = file.read()
        self._file_path = path
        return self._content

    def save_to_disk(self, path: Optional[str] = None) -> str:
        """Save text content to disk and return the path used."""
        if path is not None:
            self._file_path = path
        if self._file_path is None:
            raise ValueError("File path is not set.")
        with open(self._file_path, "w", encoding="utf-8") as file:
            file.write(self._content)
        return self._file_path


class TextEditorMainWindow(QMainWindow):
    """Main window that provides the text editor user interface."""

    def __init__(self) -> None:
        super().__init__()
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
        self.actions["new"] = new_action

        open_action = QAction(QIcon(), "Open...", self)
        open_action.setShortcut("Ctrl+O")
        open_action.setStatusTip("Open an existing text file")
        self.actions["open"] = open_action

        save_action = QAction(QIcon(), "Save", self)
        save_action.setShortcut("Ctrl+S")
        save_action.setStatusTip("Save the current document")
        self.actions["save"] = save_action

        save_as_action = QAction(QIcon(), "Save As...", self)
        save_as_action.setStatusTip("Save the current document under a new name")
        self.actions["save_as"] = save_as_action

        exit_action = QAction(QIcon(), "Exit", self)
        exit_action.setShortcut("Ctrl+Q")
        exit_action.setStatusTip("Exit the application")
        self.actions["exit"] = exit_action

        undo_action = QAction(QIcon(), "Undo", self)
        undo_action.setShortcut("Ctrl+Z")
        undo_action.setStatusTip("Undo last action")
        self.actions["undo"] = undo_action

        redo_action = QAction(QIcon(), "Redo", self)
        redo_action.setShortcut("Ctrl+Y")
        redo_action.setStatusTip("Redo last undone action")
        self.actions["redo"] = redo_action

        cut_action = QAction(QIcon(), "Cut", self)
        cut_action.setShortcut("Ctrl+X")
        cut_action.setStatusTip("Cut selection to clipboard")
        self.actions["cut"] = cut_action

        copy_action = QAction(QIcon(), "Copy", self)
        copy_action.setShortcut("Ctrl+C")
        copy_action.setStatusTip("Copy selection to clipboard")
        self.actions["copy"] = copy_action

        paste_action = QAction(QIcon(), "Paste", self)
        paste_action.setShortcut("Ctrl+V")
        paste_action.setStatusTip("Paste text from clipboard")
        self.actions["paste"] = paste_action

        about_action = QAction("About", self)
        about_action.setStatusTip("Show information about this application")
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


class TextEditorController:
    """Controller that connects the model and the main window."""

    def __init__(self, model: TextDocumentModel, view: TextEditorMainWindow) -> None:
        self._model = model
        self._view = view
        self._connect_signals()

    def _connect_signals(self) -> None:
        """Connect signals of actions to controller methods."""
        self._view.actions["new"].triggered.connect(self.new_file)
        self._view.actions["open"].triggered.connect(self.open_file)
        self._view.actions["save"].triggered.connect(self.save_file)
        self._view.actions["save_as"].triggered.connect(self.save_file_as)
        self._view.actions["exit"].triggered.connect(self._view.close)

        self._view.actions["undo"].triggered.connect(self._view.text_edit.undo)
        self._view.actions["redo"].triggered.connect(self._view.text_edit.redo)
        self._view.actions["cut"].triggered.connect(self._view.text_edit.cut)
        self._view.actions["copy"].triggered.connect(self._view.text_edit.copy)
        self._view.actions["paste"].triggered.connect(self._view.text_edit.paste)

        self._view.actions["about"].triggered.connect(self.show_about)

    def new_file(self) -> None:
        """Clear the editor and reset model state."""
        self._model.file_path = None
        self._model.content = ""
        self._view.text_edit.clear()
        self._view.statusBar().showMessage("New document", 2000)
        self._view.setWindowTitle("PyQt Text Editor")

    def open_file(self) -> None:
        """Open a text file from disk using the model."""
        path, _ = QFileDialog.getOpenFileName(
            self._view,
            "Open File",
            "",
            "Text Files (*.txt);;All Files (*)",
        )
        if not path:
            return
        try:
            content = self._model.load_from_disk(path)
        except OSError as error:
            QMessageBox.critical(self._view, "Open File", f"Could not open file:\n{error}")
            return
        self._view.text_edit.setPlainText(content)
        self._view.statusBar().showMessage(f"Opened: {path}", 2000)
        self._view.setWindowTitle(f"PyQt Text Editor - {path}")

    def save_file(self) -> None:
        """Save the current document using the model."""
        if self._model.file_path is None:
            self.save_file_as()
            return
        self._model.content = self._view.text_edit.toPlainText()
        try:
            path = self._model.save_to_disk()
        except (OSError, ValueError) as error:
            QMessageBox.critical(self._view, "Save File", f"Could not save file:\n{error}")
            return
        self._view.statusBar().showMessage(f"Saved: {path}", 2000)

    def save_file_as(self) -> None:
        """Ask for a file path and save the current document using the model."""
        path, _ = QFileDialog.getSaveFileName(
            self._view,
            "Save File As",
            "",
            "Text Files (*.txt);;All Files (*)",
        )
        if not path:
            return
        self._model.content = self._view.text_edit.toPlainText()
        try:
            used_path = self._model.save_to_disk(path)
        except OSError as error:
            QMessageBox.critical(self._view, "Save File", f"Could not save file:\n{error}")
            return
        self._view.statusBar().showMessage(f"Saved: {used_path}", 2000)
        self._view.setWindowTitle(f"PyQt Text Editor - {used_path}")

    def show_about(self) -> None:
        """Show simple About dialog."""
        QMessageBox.information(
            self._view,
            "About",
            "PyQt Text Editor\n\nExample of MVC-style PyQt application with menus and toolbars.",
        )


def main() -> None:
    """Entry point of the text editor application."""
    app = QApplication(sys.argv)
    model = TextDocumentModel()
    view = TextEditorMainWindow()
    controller = TextEditorController(model, view)
    view.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
