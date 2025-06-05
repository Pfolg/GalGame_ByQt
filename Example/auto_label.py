# -*- coding: UTF-8 -*-
"""
PROJECT_NAME GalGameStart
PRODUCT_NAME PyCharm
NAME auto_label
AUTHOR Pfolg
TIME 2025/6/1 6:39
"""
import sys
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QPushButton, QGroupBox, QLineEdit, QSizePolicy
)
from PySide6.QtCore import Qt, QTimer


class AdaptiveLabelDemo(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("QLabel宽度自适应文本")
        self.setGeometry(100, 100, 800, 600)

        # 创建主部件和布局
        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        main_layout = QVBoxLayout(main_widget)

        # 添加标题
        title = QLabel("QLabel宽度自适应文本演示")
        title.setStyleSheet("font-size: 20px; font-weight: bold; margin: 15px 0;")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        main_layout.addWidget(title)

        # 创建演示区域
        demo_container = QWidget()
        demo_layout = QHBoxLayout(demo_container)
        main_layout.addWidget(demo_container)

        # 左侧演示区
        left_group = QGroupBox("方法演示")
        left_layout = QVBoxLayout(left_group)
        demo_layout.addWidget(left_group, 1)

        # 方法1：使用大小策略
        method1_group = QGroupBox("方法1: 设置大小策略")
        method1_layout = QVBoxLayout(method1_group)

        self.label1 = QLabel("短文本")
        self.label1.setStyleSheet("background-color: #e3f2fd; border: 1px solid #90caf9; padding: 8px;")
        self.label1.setSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Fixed)
        method1_layout.addWidget(self.label1)

        btn1 = QPushButton("更改文本")
        btn1.clicked.connect(lambda: self.change_label_text(self.label1))
        method1_layout.addWidget(btn1)

        left_layout.addWidget(method1_group)

        # 方法2：使用adjustSize()
        method2_group = QGroupBox("方法2: 使用adjustSize()")
        method2_layout = QVBoxLayout(method2_group)

        self.label2 = QLabel("中等长度文本")
        self.label2.setStyleSheet("background-color: #f1f8e9; border: 1px solid #c5e1a5; padding: 8px;")
        method2_layout.addWidget(self.label2)

        btn2 = QPushButton("更改文本")
        btn2.clicked.connect(lambda: self.change_label_text(self.label2))
        method2_layout.addWidget(btn2)

        left_layout.addWidget(method2_group)

        # 方法3：固定高度策略
        method3_group = QGroupBox("方法3: 固定高度策略")
        method3_layout = QVBoxLayout(method3_group)

        self.label3 = QLabel("这是一个较长的文本示例")
        self.label3.setStyleSheet("background-color: #fff3e0; border: 1px solid #ffcc80; padding: 8px;")
        self.label3.setFixedHeight(self.label3.sizeHint().height())
        method3_layout.addWidget(self.label3)

        btn3 = QPushButton("更改文本")
        btn3.clicked.connect(lambda: self.change_label_text(self.label3))
        method3_layout.addWidget(btn3)

        left_layout.addWidget(method3_group)

        # 右侧说明区
        right_group = QGroupBox("方法说明")
        right_layout = QVBoxLayout(right_group)
        demo_layout.addWidget(right_group, 1)

        # 添加方法说明
        methods = [
            ("方法1: 设置大小策略",
             "使用 setSizePolicy() 方法：\n"
             "label.setSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Fixed)\n\n"
             "这告诉布局管理器在水平方向上优先考虑内容大小，在垂直方向上固定高度。"),

            ("方法2: 使用adjustSize()",
             "在设置文本后调用 adjustSize()：\n"
             "label.setText(new_text)\n"
             "label.adjustSize()\n\n"
             "这会强制标签立即根据新内容调整大小。"),

            ("方法3: 固定高度策略",
             "设置固定高度但宽度自适应：\n"
             "label.setFixedHeight(label.sizeHint().height())\n\n"
             "保持高度不变，让宽度随文本变化。")
        ]

        for title, content in methods:
            group = QGroupBox(title)
            layout = QVBoxLayout(group)
            label = QLabel(content)
            label.setWordWrap(True)
            layout.addWidget(label)
            right_layout.addWidget(group)

        # 添加动态演示区
        dynamic_group = QGroupBox("动态演示")
        dynamic_layout = QVBoxLayout(dynamic_group)
        main_layout.addWidget(dynamic_group)

        self.dynamic_label = QLabel("动态变化的文本")
        self.dynamic_label.setStyleSheet("""
            background-color: #fce4ec;
            border: 2px dashed #f48fb1;
            padding: 15px;
            font-size: 16px;
            border-radius: 10px;
        """)
        self.dynamic_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.dynamic_label.setSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Fixed)
        dynamic_layout.addWidget(self.dynamic_label)

        # 创建输入框和控制按钮
        input_layout = QHBoxLayout()
        self.text_input = QLineEdit()
        self.text_input.setPlaceholderText("输入新文本...")
        input_layout.addWidget(self.text_input, 3)

        update_btn = QPushButton("更新文本")
        update_btn.clicked.connect(self.update_dynamic_label)
        input_layout.addWidget(update_btn, 1)

        auto_btn = QPushButton("自动演示")
        auto_btn.clicked.connect(self.toggle_auto_demo)
        input_layout.addWidget(auto_btn, 1)

        dynamic_layout.addLayout(input_layout)

        # 自动演示定时器
        self.auto_demo_timer = QTimer()
        self.auto_demo_timer.timeout.connect(self.auto_update_text)
        self.demo_texts = [
            "短文本",
            "中等长度文本",
            "这是一个较长的文本示例",
            "非常非常长的文本，用于测试QLabel的宽度自适应能力",
            "PySide6标签宽度自适应",
            "宽度随内容变化",
            "动态调整大小",
            "QLabel自适应演示"
        ]
        self.demo_index = 0
        self.is_auto_demo = False

        # 显示初始状态
        self.statusBar().showMessage("就绪 - 标签宽度自适应演示")

    def change_label_text(self, label):
        current_text = label.text()
        if "短" in current_text:
            new_text = "这是一个较长的文本示例"
        elif "中等" in current_text:
            new_text = "非常非常长的文本，用于测试QLabel的宽度自适应能力"
        elif "较长" in current_text:
            new_text = "短文本"
        else:
            new_text = "新文本"

        label.setText(new_text)

        # 对于方法2，需要手动调用adjustSize()
        if label == self.label2:
            label.adjustSize()

    def update_dynamic_label(self):
        new_text = self.text_input.text() or "默认文本"
        self.dynamic_label.setText(new_text)
        self.text_input.clear()
        self.statusBar().showMessage(f"已更新文本: {new_text}")

    def toggle_auto_demo(self):
        self.is_auto_demo = not self.is_auto_demo

        if self.is_auto_demo:
            self.auto_demo_timer.start(1500)
            self.statusBar().showMessage("自动演示已启动...")
        else:
            self.auto_demo_timer.stop()
            self.statusBar().showMessage("自动演示已停止")

    def auto_update_text(self):
        self.dynamic_label.setText(self.demo_texts[self.demo_index])
        self.demo_index = (self.demo_index + 1) % len(self.demo_texts)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = AdaptiveLabelDemo()
    window.show()
    sys.exit(app.exec())
