from typing   import Optional

from PyQt5 import Qt

from vspreview.core  import AbstractMainWindow, AbstractToolbar, Frame
from vspreview.utils import debug, set_qobject_names


class DebugToolbar(AbstractToolbar):
    __slots__ = (
        'test_button',
        'exec_lineedit', 'exec_button',
        'test_button',
        'toggle_button',
    )

    def __init__(self, main: AbstractMainWindow) -> None:
        super().__init__(main, 'Debug')

        self.setup_ui()

        self.  test_button.clicked.connect(self.test_button_clicked)
        self.  exec_button.clicked.connect(self.exec_button_clicked)
        self.exec_lineedit.editingFinished.connect(self.exec_button_clicked)

        if self.main.DEBUG_TOOLBAR_BUTTONS_PRINT_STATE:
            self.filter = debug.EventFilter(self)
            self.main.toolbars.main.widget.installEventFilter(self.filter)
            for toolbar in self.main.toolbars:
                toolbar.widget.installEventFilter(self.filter)

        set_qobject_names(self)

    def setup_ui(self) -> None:
        layout = Qt.QHBoxLayout(self)
        layout.setObjectName('DebugToolbar.setup_ui.layout')
        layout.setContentsMargins(0, 0, 0, 0)

        self.test_button = Qt.QPushButton(self)
        self.test_button.setText('Test')
        layout.addWidget(self.test_button)

        self.exec_lineedit = Qt.QLineEdit(self)
        self.exec_lineedit.setPlaceholderText(
            'Python statement in context of DebugToolbar.exec_button_clicked()')
        layout.addWidget(self.exec_lineedit)

        self.exec_button = Qt.QPushButton(self)
        self.exec_button.setText('Exec')
        layout.addWidget(self.exec_button)

        layout.addStretch()

        self.toggle_button.setVisible(False)


    def test_button_clicked(self, checked: Optional[bool] = None) -> None:
        pass

    def exec_button_clicked(self, checked: Optional[bool] = None) -> None:
        try:
            exec(self.exec_lineedit.text())  # pylint: disable=exec-used
        except Exception as e:  # pylint: disable=broad-except
            print(e)
