# -*- coding: UTF-8 -*-
"""
PROJECT_NAME GalGameStart
PRODUCT_NAME PyCharm
NAME sidebar
AUTHOR Pfolg
TIME 2025/5/31 16:30
"""
import sys
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QPushButton, QVBoxLayout,
    QLabel, QGraphicsDropShadowEffect
)
from PySide6.QtCore import QPropertyAnimation, QEasingCurve, Qt
from PySide6.QtGui import QColor


class SideMenu(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent = parent
        self.is_visible = False

        # 初始设置 - 隐藏在屏幕左侧
        screen_rect = QApplication.primaryScreen().availableGeometry()
        self.setGeometry(-int(0.2 * screen_rect.width()), 0,
                         int(0.2 * screen_rect.width()),
                         screen_rect.height())

        self.setup_ui()
        self.apply_styles()
        self.setup_animation()
        self.add_shadow_effect()

    def setup_ui(self):
        """设置菜单内容"""
        layout = QVBoxLayout()
        layout.setContentsMargins(15, 30, 15, 30)
        layout.setSpacing(15)

        # 标题
        title = QLabel("导航菜单")
        title.setAlignment(Qt.AlignCenter)
        title.setObjectName("menuTitle")
        layout.addWidget(title)

        # 菜单项
        menu_items = [
            ("🏠 首页", "home"),
            ("📁 项目", "projects"),
            ("📊 分析", "analytics"),
            ("⚙️ 设置", "settings"),
            ("❓ 帮助", "help")
        ]

        for text, obj_name in menu_items:
            btn = QPushButton(text)
            btn.setObjectName(obj_name)
            btn.setCursor(Qt.PointingHandCursor)
            layout.addWidget(btn)

        # 底部按钮
        close_btn = QPushButton("关闭菜单")
        close_btn.setObjectName("closeBtn")
        close_btn.clicked.connect(self.toggle_menu)
        layout.addStretch(1)
        layout.addWidget(close_btn)

        self.setLayout(layout)

    def apply_styles(self):
        """应用CSS样式"""
        self.setStyleSheet("""
            /* 主菜单容器 */
            SideMenu {
                background-color: #2c3e50;
                border-top-right-radius: 15px;
                border-bottom-right-radius: 15px;
                border-right: 2px solid #3498db;
            }

            /* 标题样式 */
            #menuTitle {
                color: #ecf0f1;
                font-size: 24px;
                font-weight: bold;
                padding: 15px 0;
                border-bottom: 2px solid #3498db;
                margin-bottom: 20px;
            }

            /* 菜单按钮通用样式 */
            QPushButton {
                background-color: rgba(52, 152, 219, 0.3);
                color: #ecf0f1;
                font-size: 16px;
                text-align: left;
                padding: 15px 20px;
                border: none;
                border-radius: 8px;
                transition: all 0.3s ease;
            }

            /* 按钮悬停效果 */
            QPushButton:hover {
                background-color: rgba(52, 152, 219, 0.7);
                transform: translateX(10px);
            }

            /* 按钮按下效果 */
            QPushButton:pressed {
                background-color: rgba(41, 128, 185, 0.9);
            }

            /* 关闭按钮特殊样式 */
            #closeBtn {
                background-color: rgba(231, 76, 60, 0.4);
                text-align: center;
            }

            #closeBtn:hover {
                background-color: rgba(231, 76, 60, 0.7);
            }
        """)

    def setup_animation(self):
        """设置显示/隐藏动画"""
        self.animation = QPropertyAnimation(self, b"pos")
        self.animation.setDuration(350)  # 动画持续时间
        self.animation.setEasingCurve(QEasingCurve.OutCubic)  # 平滑的缓动曲线

    def add_shadow_effect(self):
        """添加阴影效果"""
        shadow = QGraphicsDropShadowEffect(self)
        shadow.setBlurRadius(25)
        shadow.setColor(QColor(0, 0, 0, 180))
        shadow.setOffset(5, 0)  # 阴影向右偏移
        self.setGraphicsEffect(shadow)

    def toggle_menu(self):
        """切换菜单显示状态"""
        self.is_visible = not self.is_visible

        # 获取当前屏幕尺寸
        screen_rect = QApplication.primaryScreen().availableGeometry()
        menu_width = self.width()

        # 设置动画起始和结束位置
        if self.is_visible:
            start_pos = self.pos()
            end_pos = self.pos().setX(0)
        else:
            start_pos = self.pos()
            end_pos = self.pos().setX(-menu_width)

        self.animation.setStartValue(start_pos)
        self.animation.setEndValue(end_pos)
        self.animation.start()


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("带动画的侧边菜单")
        self.setMinimumSize(800, 600)

        # 创建主内容区域
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        layout = QVBoxLayout(central_widget)
        layout.setContentsMargins(50, 50, 50, 50)

        # 标题
        title = QLabel("带动画的侧边菜单演示")
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("""
            font-size: 28px;
            font-weight: bold;
            color: #2c3e50;
            margin-bottom: 30px;
        """)
        layout.addWidget(title)

        # 切换菜单按钮
        toggle_btn = QPushButton("显示/隐藏菜单")
        toggle_btn.setStyleSheet("""
            QPushButton {
                background-color: #3498db;
                color: white;
                font-size: 18px;
                padding: 15px;
                border-radius: 8px;
                min-width: 200px;
            }
            QPushButton:hover {
                background-color: #2980b9;
            }
        """)
        toggle_btn.setCursor(Qt.PointingHandCursor)
        layout.addWidget(toggle_btn, alignment=Qt.AlignCenter)

        # 创建侧边菜单
        self.side_menu = SideMenu(self)

        # 连接按钮事件
        toggle_btn.clicked.connect(self.side_menu.toggle_menu)

        # 应用全局样式
        self.setStyleSheet("""
            QMainWindow {
                background-color: #ecf0f1;
                font-family: 'Segoe UI', Arial, sans-serif;
            }
        """)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
