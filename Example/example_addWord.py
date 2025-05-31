# -*- coding: UTF-8 -*-
"""
PROJECT_NAME GalGameStart
PRODUCT_NAME PyCharm
NAME example_addWord
AUTHOR Pfolg
TIME 2025/5/27 20:48
"""
from PySide6.QtWidgets import QApplication, QMainWindow, QTextEdit, QPushButton
from PySide6.QtCore import QTimer
from PySide6.QtGui import QTextCursor


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        # 初始化界面
        self.setWindowTitle("逐个添加文字示例")
        self.setGeometry(100, 100, 400, 300)

        # 创建QTextEdit
        self.text_edit = QTextEdit(self)
        self.text_edit.setGeometry(0, 100, 400, 300)
        # self.setCentralWidget(self.text_edit)
        self.text_edit.setStyleSheet("background-color:lightblue;")
        self.text_edit.setReadOnly(True)
        # 按钮
        self.btn = QPushButton(self)
        self.btn.setGeometry(0, 0, 75, 24)
        self.btn.setText("再来一遍")
        self.btn.clicked.connect(self.try2)

        self.pause = QPushButton(self)
        self.pause.setGeometry(80, 0, 75, 24)
        self.pause.setText("暂停")
        self.pause.clicked.connect(self.ppause)

        self.start = QPushButton(self)
        self.start.setGeometry(160, 0, 75, 24)
        self.start.setText("继续")
        self.start.clicked.connect(self.sstart)

        # 预添加的文本
        self.text_to_add = "Hello, 这是逐个添加的文字效果！"
        self.current_index = 0  # 当前添加位置的索引

        # 初始化定时器
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.add_next_char)
        self.speed = 100
        self.timer.start(self.speed)

    def ppause(self):
        self.timer.stop()

    def sstart(self):
        self.timer.start()

    def try2(self):
        self.current_index = 0
        self.speed = 50
        self.timer = None
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.add_next_char)
        self.timer.start(self.speed)
        self.text_edit.clear()
        self.text_to_add = "你好呀，这是再来一次要添加的文字，请欣赏效果！"
        self.timer.start()

    def add_next_char(self):
        if self.current_index < len(self.text_to_add):
            # 获取下一个字符
            next_char = self.text_to_add[self.current_index]

            # 移动光标到末尾并插入字符
            self.text_edit.moveCursor(QTextCursor.End)
            self.text_edit.insertPlainText(next_char)

            self.current_index += 1
        else:
            self.timer.stop()  # 停止定时器


if __name__ == "__main__":
    app = QApplication([])
    window = MainWindow()
    window.show()
    app.exec()
