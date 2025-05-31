# -*- coding: UTF-8 -*-
"""
PROJECT_NAME GalGameStart
PRODUCT_NAME PyCharm
NAME test_ui
AUTHOR Pfolg
TIME 2025/5/27 20:36
"""
import sys
import time

from PySide6.QtCore import Qt, QTimer
from PySide6.QtUiTools import QUiLoader
from PySide6.QtWidgets import QApplication, QTextEdit


def add_text(target: QTextEdit, text: str):
    for i in text:
        target.append(i)
        time.sleep(1 / speed)


speed = 30
app = QApplication(sys.argv)
loader = QUiLoader()
ui = loader.load("test.ui")
ui.setWindowFlags(
    Qt.WindowType.Window |
    # Qt.WindowType.WindowMaximizeButtonHint |
    Qt.WindowType.WindowCloseButtonHint
)
ui.show()
timer = QTimer()
a: QTextEdit = ui.textEdit
timer.timeout.connect(
    lambda: add_text(a, "在Galgame中，文字显示速度（即每个字符的打印时间）通常受多种因素影响，但以下是一般情况下的分析："))
timer.setSingleShot(True)
a.textChanged.connect(lambda: timer.start())

sys.exit(app.exec())
