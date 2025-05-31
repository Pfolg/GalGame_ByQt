# -*- coding: UTF-8 -*-
"""
PROJECT_NAME GalGameStart
PRODUCT_NAME PyCharm
NAME manage_window
AUTHOR Pfolg
TIME 2025/5/29 11:02
"""
# 进行窗口管理的模块

import sys

from PIL.ImageQt import QPixmap
from PySide6 import QtCore
from PySide6.QtCore import Qt, QSize, QPropertyAnimation, QPoint, QByteArray, QTimer
from PySide6.QtGui import QAction, QIcon, QFont, QColor
from PySide6.QtUiTools import QUiLoader
from PySide6.QtWidgets import QWidget, QApplication, QCheckBox, QLineEdit, QPushButton, QTextEdit, QInputDialog, \
    QMessageBox, QLabel, QMenu, QToolButton, QGraphicsDropShadowEffect, QGraphicsOpacityEffect

import manage_data as mda
import process_data as pda

# 载入数据
data_class = mda.ManageData()
phot_data = mda.convert_value_to_str(mda.read_manifest(data_class.phot_manifest))
ui_data = mda.read_manifest(data_class.ui_manifest)
font_data = mda.convert_value_to_str(mda.read_manifest(data_class.font_manifest))


# 读取屏幕长宽
def get_screen_info() -> tuple:
    # 获取现有的 QApplication 实例
    _app = QApplication.instance()

    if _app is not None:
        screen = _app.primaryScreen().geometry()

        return screen.width(), screen.height()
    else:
        return 0, 0


# 修改文件数据的窗口
class DataChanger(QWidget):
    def __init__(self):
        super().__init__()
        # 加载Ui
        loader = QUiLoader()
        ui_file = ui_data.get("develop")
        loader.load(ui_file, self)
        # 获取屏幕参数
        self.screen_size = get_screen_info()
        # 获取部件
        self.checkbox: QCheckBox = self.findChild(QCheckBox, "checkBox")
        self.lineEdit: QLineEdit = self.findChild(QLineEdit, "lineEdit")
        self.pushButton: QPushButton = self.findChild(QPushButton, "pushButton")
        self.pushButton2: QPushButton = self.findChild(QPushButton, "pushButton_2")
        self.textEdit: QTextEdit = self.findChild(QTextEdit, "textEdit")
        # 初始化窗口
        self.setup_ui()
        # 绑定功能
        self.bind_functions()

    def bind_functions(self) -> None:
        self.lineEdit.setPlaceholderText("{'name':'developer',...}")
        self.checkbox.clicked.connect(self.on_change_checkbox_value)
        self.pushButton.clicked.connect(self.change_data)
        self.pushButton2.clicked.connect(self.add_content)
        # self.change_enable(False)

    @staticmethod
    def change_user_data(data: dict):
        origin_data: dict = pda.load_user_data(data_class.file_user)
        for k, v in data.items():
            if k not in origin_data.keys():
                continue
            # 更新数据
            origin_data[k] = v
        # 写入文件
        pda.save_user_data(data_class.file_user, origin_data)

    # 收集需要显示的数据
    @staticmethod
    def collect_data() -> dict:
        return pda.load_user_data(data_class.file_user)

    # 修改数据->文件，直接修改文件可能会被覆盖
    # 直接修改内存中的数据又可能导致数据不能马上生效
    # >>>综上，在关闭应用的情况下进行数据修改！<<<
    def change_data(self) -> None:
        content = self.lineEdit.text()
        try:
            my_data = eval(content)
            if not isinstance(my_data, dict):
                QMessageBox.warning(self, "Warning", "输入非字典！")
                return
            else:
                self.change_user_data(my_data)
                QMessageBox.information(self, "Message", "修改了配置文件的数据！")
        except NameError:
            QMessageBox.critical(self, "Error", "非正常输入！")
            return
        except Exception as e:
            QMessageBox.critical(self, "Error", f"遇到错误：{e}")

    # 更改输入框和按钮的可用状态
    def change_enable(self, b: bool) -> None:
        self.lineEdit.setEnabled(b)
        self.pushButton.setEnabled(b)

    # 更改textedit显示内容
    def add_content(self, content=None) -> None:
        if not content:
            content = self.collect_data()
        self.textEdit.clear()
        self.textEdit.setText(str(content))

    # checkbox逻辑
    def on_change_checkbox_value(self) -> None:
        # 取消选定不需要验证
        if not self.checkbox.isChecked():
            self.checkbox.setChecked(False)
            self.change_enable(False)
            return
        r1, r2 = QInputDialog.getText(
            self, "开发者验证", "请输入密码", QLineEdit.EchoMode.Normal,
            text="")  # PasswordEchoOnEdit
        if r2:
            # 酌情更改
            if r1 == "我是开发者":
                self.checkbox.setChecked(True)
                self.change_enable(True)
            else:
                self.checkbox.setChecked(False)
                self.change_enable(False)
        else:
            self.checkbox.setChecked(False)
            self.change_enable(False)

    # 初始化UI
    def setup_ui(self) -> None:
        w, h = 400, 300
        self.setGeometry(int((self.screen_size[0] - w) / 2), int((self.screen_size[1] - h) / 2), w, h)
        self.setWindowTitle("DataChanger")
        self.setMaximumSize(w, h)


# 背景类
class WidgetBackground(QWidget):
    def __init__(self, parent):
        super().__init__()
        self.setParent(parent)
        self.background_picture = None
        self.background_label = QLabel(self)
        self.logo_label = QLabel(self)

    def set_bg(self, picture: str) -> None:
        self.background_label.setPixmap(QPixmap(picture))

    def set_logo(self, picture: str) -> None:
        self.logo_label.setPixmap(QPixmap(picture))

    def init_ui(self, x: int, y: int) -> None:
        self.setGeometry(0, 0, x, y)
        self.background_label.setGeometry(0, 0, x, y)
        self.background_label.setScaledContents(True)
        logo_size = .18
        self.logo_label.setGeometry(int(.02 * x), int(.8 * y), int(logo_size * x), int(logo_size * y))
        self.logo_label.setScaledContents(True)


# 交互UI界面
class WidgetCommunication(QWidget):
    def __init__(self, parent):
        super().__init__()
        self.setParent(parent)
        # 加载字体
        self.font_family = pda.load_font(font_data.get("MapleMono-NF-CN-Medium"))
        # 对话框
        self.dialog = QTextEdit(self)
        # 按钮组
        self.btn_back = QPushButton(self)
        self.btn_head = QPushButton(self)
        self.btn_bookmark = QToolButton(self)
        self.btn_automatic = QPushButton(self)
        self.btn_menu = QPushButton(self)
        self.btns = [self.btn_back, self.btn_head, self.btn_menu, self.btn_bookmark, self.btn_automatic]
        # 选项窗口
        self.widget_choice = QWidget(self)
        self.btn_choice1 = QPushButton(self.widget_choice)
        self.btn_choice2 = QPushButton(self.widget_choice)
        self._choice_num: int = 0  # 0、1
        # 输入窗口
        self.widget_input = QWidget(self)
        self.input_label = QLabel(self.widget_input)
        self.input_line = QLineEdit(self.widget_input)
        self.input_hand = QPushButton(self.widget_input)
        self._input_content: str = ""
        # 确认窗口
        self.widget_confirm = QWidget(self)
        self.confirm_label = QLabel(self.widget_confirm)
        self.confirm_btn_yes = QPushButton(self.widget_confirm)
        self.confirm_btn_no = QPushButton(self.widget_confirm)
        self.confirm_bool: bool = False
        # 消息窗口
        self.widget_info = QWidget(self)
        self.info_line = QTextEdit(self.widget_info)
        # 消息fade
        # 创建淡入淡出效果
        self.opacity_effect = QGraphicsOpacityEffect(self.info_line)
        self.info_line.setGraphicsEffect(self.opacity_effect)
        self.opacity_effect.setOpacity(1.0)  # 初始完全不透明
        # 创建淡出动画
        self.fade_out_animation = QPropertyAnimation(self.opacity_effect, QByteArray(b"opacity"))
        self.fade_out_animation.setDuration(500)  # 0.5秒淡出时间
        self.fade_out_animation.setStartValue(1.0)
        self.fade_out_animation.setEndValue(0.0)
        self.fade_out_animation.finished.connect(self.info_line.hide)
        # 创建定时器
        self.hide_timer = QTimer()
        self.hide_timer.setSingleShot(True)
        # 连接动画
        self.hide_timer.timeout.connect(self.fade_out_animation.start)

    def select_confirm_yes(self) -> None:
        self.confirm_bool = True
        self.widget_confirm.hide()

    def select_confirm_no(self) -> None:
        self.confirm_bool = False
        self.widget_confirm.hide()

    def setup_confirm_w(self) -> None:
        self.widget_confirm.setObjectName("widget_confirm")
        self.widget_confirm.setStyleSheet(
            """
            #widget_confirm{
            background-color: rgba(170, 255, 255,.3);
            border: 1px solid rgba(255, 255, 127,.2);
            border-radius: 10px;
            }
            QPushButton {
                background-color: rgba(170, 255, 255,.5);
                border: 1px solid rgba(255, 255, 127,.5);
                border-radius: 20px;
                padding: 8px 15px;
                min-width: 80px;
                min-height: 30px;
                color: #333;
            }
            QPushButton:hover {
                background-color: rgba(170, 255, 255,.7);
                border: 1px solid rgba(255, 255, 127,.7);
            }
            QPushButton:pressed {
                background-color: rgb(255, 255, 255);
                border: 1px solid rgb(255, 255, 255);
            }
                
            """
        )
        self.confirm_label.setGeometry(
            int(.1 * self.widget_confirm.width()), int(.2 * self.widget_confirm.height()),
            int(.8 * self.widget_confirm.width()), int(.2 * self.widget_confirm.height())
        )
        self.confirm_btn_yes.setGeometry(
            int(.2 * self.widget_confirm.width()), int(.6 * self.widget_confirm.height()),
            int(.2 * self.widget_confirm.width()), int(.2 * self.widget_confirm.height())
        )
        self.confirm_btn_no.setGeometry(
            int(.6 * self.widget_confirm.width()), int(.6 * self.widget_confirm.height()),
            int(.2 * self.widget_confirm.width()), int(.2 * self.widget_confirm.height())
        )
        self.confirm_label.setFont(QFont(self.font_family, 20))
        self.confirm_btn_yes.setFont(QFont(self.font_family, 20))
        self.confirm_btn_no.setFont(QFont(self.font_family, 20))
        self.confirm_label.setText("Question content")
        self.confirm_btn_yes.setText("YES")
        self.confirm_btn_no.setText("NO")
        self.confirm_btn_yes.clicked.connect(self.select_confirm_yes)
        self.confirm_btn_no.clicked.connect(self.select_confirm_no)

    def setup_info_w(self) -> None:
        # 定义位置
        self.info_line.setGeometry(0, 0, self.widget_info.width(), self.widget_info.height())
        # 设置样式
        self.info_line.setStyleSheet(
            "background-color: rgba(170, 255, 255,.3);"
            "border: 1px solid rgba(255, 255, 127,.2);"
            "border-radius: 10px;"
            "padding:4px,8px,4px,8px"
        )
        # 设置字体
        self.info_line.setFont(QFont(self.font_family, 18))
        # 初始状态为隐藏
        self.info_line.hide()
        # 完全只读
        self.info_line.setTextInteractionFlags(Qt.TextInteractionFlag.NoTextInteraction)

    def showMessage(self, msg: str, duration=5000) -> None:
        # 1. 停止所有正在进行的动画和定时器
        if self.hide_timer.isActive():
            self.hide_timer.stop()

        if self.fade_out_animation.state() == QPropertyAnimation.State.Running:
            self.fade_out_animation.stop()

        # 2. 重置透明度为完全不透明
        self.opacity_effect.setOpacity(1.0)

        # 3. 确保控件可见
        self.info_line.show()

        # 4. 设置新消息内容
        self.info_line.setMarkdown(msg)

        # 5. 启动新定时器
        self.hide_timer.start(duration)

    def setup_input_w(self) -> None:
        # 设置按钮大小位置
        ww, wh = self.widget_choice.width(), self.widget_choice.height()
        self.input_label.setGeometry(int(.1 * ww), int(.3 * wh), int(.8 * ww), int(.2 * wh))
        self.input_line.setGeometry(int(.1 * ww), int(.5 * wh), int(.7 * ww), int(.16 * wh))
        self.input_hand.setGeometry(int(.82 * ww), int(.5 * wh), int(.1 * ww), int(.16 * wh))
        self.input_label.setText("你的名字是？")
        self.input_hand.setFont(QFont(self.font_family, 24))
        self.input_hand.setText("✔")
        for i in [self.input_label, self.input_line]:
            # 设置字体
            i.setFont(QFont(self.font_family, 20))
        self.input_label.setStyleSheet(
            "background-color: rgba(255, 255, 255, 0);"
            "border: 1px solid rgba(255, 255, 127, 0);"
            "border-radius: 10px;"
        )
        self.input_line.setStyleSheet(
            """
                background-color: rgba(170, 255, 255,.5);
                border: 1px solid rgba(255, 255, 127,.2);
                border-radius: 10px;
            """
        )
        self.input_hand.setStyleSheet(
            """
                QPushButton {
                    background-color: rgba(170, 255, 255,.5);
                    border: 1px solid rgba(255, 255, 127,.5);
                    border-radius: 10px;
                    padding: 8px 15px;
                    min-width: 80px;
                    min-height: 30px;
                    color: #333;
                }
                QPushButton:hover {
                    background-color: rgba(170, 255, 255,.7);
                    border: 1px solid rgba(255, 255, 127,.7);
                }
                QPushButton:pressed {
                    background-color: rgb(255, 255, 255);
                    border: 1px solid rgb(255, 255, 255);
                }
                """
        )
        self.widget_input.hide()
        self.input_line.returnPressed.connect(self.form_question)
        self.input_hand.clicked.connect(self.form_question)

    def form_question(self) -> None:
        answer = self.input_line.text()
        if answer:
            self._input_content = answer
            self.widget_input.hide()
        else:
            self.showMessage("<span style='color:red'>输入为空！</span>")

    def set_question(self, q: str) -> None:
        self.input_label.setText(q)
        self.widget_input.show()

    def setup_choice_w(self) -> None:
        # 设置按钮大小位置
        ww, wh = self.widget_choice.width(), self.widget_choice.height()
        self.btn_choice1.setGeometry(int(.1 * ww), int(.1 * wh), int(.8 * ww), int(.3 * wh))
        self.btn_choice2.setGeometry(int(.1 * ww), int(.6 * wh), int(.8 * ww), int(.3 * wh))

        # 设置文字
        self.set_choice("选项一", "选项二")
        for i in [self.btn_choice1, self.btn_choice2]:
            # 设置字体
            i.setFont(QFont(self.font_family, 20))
            # 设置样式
            i.setStyleSheet(
                """
                QPushButton {
                    background-color: rgba(255, 255, 255, 0.5);
                    border: 1px solid rgba(100, 100, 100, 0.5);
                    border-radius: 10px;
                    padding: 8px 15px;
                    min-width: 80px;
                    min-height: 30px;
                    color: #333;
                }
                QPushButton:hover {
                    background-color: rgba(98, 209, 210, 0.7);
                    border: 1px solid rgba(100, 100, 100, 0.5);
                }
                QPushButton:pressed {
                    background-color: rgb(84, 113, 254);
                    border: 1px solid rgba(80, 80, 80, 0.7);
                }
                """
            )
        # 绑定功能
        self.btn_choice1.clicked.connect(self.select_choice1)
        self.btn_choice2.clicked.connect(self.select_choice2)

        # 初始状态为隐藏
        self.widget_choice.hide()

    def select_choice1(self) -> None:
        self._choice_num = 0
        self.widget_choice.hide()

    def select_choice2(self) -> None:
        self._choice_num = 1
        self.widget_choice.hide()

    def set_choice(self, choice1: str, choice2: str) -> None:
        self.btn_choice1.setText(choice1)
        self.btn_choice2.setText(choice2)
        self.widget_choice.show()

    def function_bookmark(self) -> None:
        menu = QMenu(self.btn_bookmark)
        action_add = QAction(parent=menu)
        menu_load = QMenu(parent=menu)
        menu_delete = QMenu(parent=menu)

        action_add.setText("添加")
        menu_load.setTitle("加载")
        menu_delete.setTitle("删除")

        menu.addAction(action_add)
        menu.addMenu(menu_load)
        menu.addMenu(menu_delete)
        self.btn_bookmark.setMenu(menu)
        self.btn_bookmark.setAutoRaise(True)
        self.btn_bookmark.setPopupMode(QToolButton.ToolButtonPopupMode.InstantPopup)

    def init_dialog_btn(self, x: int, y: int) -> None:
        self.setGeometry(0, 0, x, y)
        self.dialog.setGeometry(int(.2 * x), int(.75 * y), int(.6 * x), int(.2 * y))
        # 设置样式
        self.dialog.setStyleSheet(
            """
            QTextEdit{
                background-color: rgba(170, 255, 255,.3);
                border: 1px solid rgba(255, 255, 127,.3);
                border-radius: 20px;
                padding: 4px 12px 4px 12px;  
                }              
            """
        )
        # 设置字体
        self.dialog.setFont(QFont(self.font_family, 18))
        self.dialog.setMarkdown(
            "### Hello, World![三级标题]\n你好，世界！\n#### 四级标题\n\n<span style='color:red'>重生之我在CUIT当学渣</span>")
        # 对话框只读模式
        # self.dialog.setReadOnly(True)
        self.dialog.setTextInteractionFlags(Qt.TextInteractionFlag.NoTextInteraction)
        # 按钮位置设定
        btn_w, btn_h = int(.04 * x), int(.04 * y)
        # 计算底线x、y
        standardLastX = (self.dialog.x() + self.dialog.width() - btn_w) / x
        standardLastY = (self.dialog.y() + self.dialog.height() + btn_h * .2) / y
        # 步长
        step = .05
        self.btn_menu.setGeometry(int(standardLastX * x), int(standardLastY * y), btn_w, btn_h)
        self.btn_bookmark.setGeometry(int((standardLastX - step) * x), int(standardLastY * y), btn_w, btn_h)
        self.btn_automatic.setGeometry(int((standardLastX - 2 * step) * x), int(standardLastY * y), btn_w, btn_h)
        self.btn_head.setGeometry(int((standardLastX - 3 * step) * x), int(standardLastY * y), btn_w, btn_h)
        self.btn_back.setGeometry(int((standardLastX - 4 * step) * x), int(standardLastY * y), btn_w, btn_h)
        self.btn_back.setIcon(QIcon(phot_data.get("btn_back")))
        self.btn_head.setIcon(QIcon(phot_data.get("btn_head")))
        self.btn_menu.setIcon(QIcon(phot_data.get("btn_menu")))
        self.btn_bookmark.setIcon(QIcon(phot_data.get("btn_bookmark")))
        self.btn_automatic.setIcon(QIcon(phot_data.get("btn_automatic_play")))
        self.btn_head.setToolTip("下页")
        self.btn_back.setToolTip("上页")
        self.btn_menu.setToolTip("菜单")
        self.btn_bookmark.setToolTip("书签")
        self.btn_automatic.setToolTip("自动")
        white_ratio = .2
        for btn in self.btns:
            btn.setStyleSheet(f"background-color: rgba(255, 255, 255,{white_ratio});")
            btn.setIconSize(QSize(24, 24))

        self.widget_choice.setGeometry(int(.3 * x), int(.2 * y), int(.4 * x), int(.4 * y))
        self.widget_input.setGeometry(int(.3 * x), int(.4 * y), int(.4 * x), int(.4 * y))
        self.widget_confirm.setGeometry(int(.3 * x), int(.2 * y), int(.4 * x), int(.4 * y))
        self.widget_info.setGeometry(int(.8 * x), 0, int(.2 * x), int(.2 * y))
        # self.widget_choice.setStyleSheet(
        #     "background-color: rgba(170, 255, 255,.3);"
        #     "border: 1px solid rgba(255, 255, 127,.2);"
        #     "border-radius: 10px;"
        # )
        # self.widget_input.setStyleSheet(
        #     "background-color: rgba(170, 255, 255,.3);"
        #     "border: 1px solid rgba(255, 255, 127,.2);"
        #     "border-radius: 10px;"
        # )

        self.setup_choice_w()
        self.setup_input_w()
        self.setup_confirm_w()
        self.setup_info_w()

        self.function_bookmark()

        # self.widget_choice.show()
        # self.widget_input.show()


# ESC菜单
class WidgetEsc(QWidget):
    def __init__(self, parent):
        super().__init__()
        self.setParent(parent)
        self.is_visible = False
        # ESC菜单动画总开关
        self.isUsing = True
        # self.animation = QPropertyAnimation(self, b"pos")
        self.animation = QPropertyAnimation(self, QByteArray(b"pos"))
        self.label_logo = QLabel(self)  # logo
        self.btn_continue = QPushButton(self)  # 继续游戏
        self.btn_newGame = QPushButton(self)  # 新游戏
        self.btn_setting = QPushButton(self)  # 设置
        self.btn_login = QPushButton(self)  # 登录界面
        self.btn_about = QPushButton(self)  # 关于
        self.btn_quit = QPushButton(self)  # 退出
        self.btns = [
            self.btn_continue, self.btn_newGame, self.btn_setting,
            self.btn_login, self.btn_about, self.btn_quit
        ]

    def apply_styles(self):
        """应用CSS样式"""
        """
        *{
            background - color: rgba(98, 209, 210, 0.1);
        }
        """
        self.setStyleSheet("""            
            /* 菜单按钮通用样式 */
            QPushButton {
                background-color: rgba(52, 152, 219, 0.3);
                color: #ecf0f1;
                font-size: 20px;
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
        """)

    def setup_animation(self):
        """设置显示/隐藏动画"""
        self.animation.setDuration(350)  # 动画持续时间
        self.animation.setEasingCurve(QtCore.QEasingCurve.Type.OutCubic)  # 平滑的缓动曲线

    def add_shadow_effect(self):
        """添加阴影效果"""
        shadow = QGraphicsDropShadowEffect(self)
        shadow.setBlurRadius(25)
        shadow.setColor(QColor(0, 0, 0, 180))
        shadow.setOffset(5, 0)  # 阴影向右偏移
        self.setGraphicsEffect(shadow)

    def toggle_menu(self) -> None:
        """切换菜单显示状态"""
        # 如果动画正在运行，先停止
        if self.animation.state() == QPropertyAnimation.State.Running:
            self.animation.stop()
        self.is_visible = not self.is_visible
        if not self.isUsing:
            self.is_visible = False

        # 获取当前菜单宽度
        menu_width = self.width()
        current_pos = self.pos()

        # 设置动画起始位置（当前位置）
        self.animation.setStartValue(current_pos)

        if self.is_visible:
            # 显示菜单：移动到(0, y)位置
            end_pos = QPoint(0, current_pos.y())
        else:
            # 隐藏菜单：移动到屏幕左侧外(-menu_width, y)位置
            end_pos = QPoint(-menu_width, current_pos.y())

        self.animation.setEndValue(end_pos)
        self.animation.start()

    def init_ui(self, x: int, y: int) -> None:
        self.setGeometry(-int(.4 * x), 0, int(.4 * x), y)
        self.label_logo.setGeometry(
            int(.05 * self.width()),
            int(.05 * self.height()),
            int(.6 * self.width()),
            int(.2 * self.height()))
        _x, _y, w, h, step = (
            int(.05 * self.width()),
            int(.3 * self.height()),
            int(.6 * self.width()),
            int(.08 * self.height()),
            int(.1 * self.height())
        )
        __btn_words = ["继续游戏", "新游戏", "设置", "登录界面", "关于", "退出"]
        font = pda.load_font(font_data.get("MapleMono-NF-CN-Medium"))
        for i in range(len(self.btns)):
            self.btns[i].setGeometry(_x, int(_y + step * i), w, h)
            self.btns[i].setText(__btn_words[i])
            self.btns[i].setFont(QFont(font, 20))

        self.label_logo.setScaledContents(True)
        self.label_logo.setPixmap(QPixmap(phot_data.get("logo_test")))
        self.btn_continue.clicked.connect(self.toggle_menu)
        self.apply_styles()
        self.setup_animation()
        self.add_shadow_effect()


class WidgetLogin(QWidget):
    def __init__(self, parent):
        super().__init__()
        self.setParent(parent)
        self.label_background = QLabel(self)
        self.label_logo = QLabel(self)  # logo
        self.btn_continue = QPushButton(self)  # 继续游戏
        self.btn_newGame = QPushButton(self)  # 新游戏
        self.btn_setting = QPushButton(self)  # 设置
        self.btn_about = QPushButton(self)  # 关于
        self.btn_quit = QPushButton(self)  # 退出
        self.btns = [
            self.btn_continue, self.btn_newGame, self.btn_setting,
            self.btn_about, self.btn_quit
        ]

    def init_ui(self, x: int, y: int) -> None:
        __btn_words = ["继续游戏", "新游戏", "设置", "关于", "退出"]
        font = pda.load_font(font_data.get("MapleMono-NF-CN-Medium"))
        self.setGeometry(0, 0, x, y)
        self.label_background.setGeometry(0, 0, x, y)
        self.label_logo.setScaledContents(True)
        self.label_background.setScaledContents(True)
        self.label_background.setPixmap(QPixmap(phot_data.get("bg_login_test")))
        self.label_logo.setGeometry(int(.35 * x), int(.1 * y), int(.3 * x), int(.2 * y))
        self.label_logo.setPixmap(QPixmap(phot_data.get("logo_test")))
        _x, _y, w, h, step = (
            int(.3 * self.width()),
            int(.4 * self.height()),
            int(.4 * self.width()),
            int(.08 * self.height()),
            int(.1 * self.height())
        )
        for i in range(len(self.btns)):
            self.btns[i].setGeometry(_x, int(_y + step * i), w, h)
            self.btns[i].setText(__btn_words[i])
            self.btns[i].setFont(QFont(font, 28))

        self.apply_styles()
        self.hide()

    def apply_styles(self):
        """应用CSS样式"""
        self.setStyleSheet("""            
            /* 菜单按钮通用样式 */
            QPushButton {
                background-color: rgba(52, 152, 219, 0.3);
                color: #ecf0f1;
                font-size: 28px;
                text-align: center;
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
        """)


# 主窗口
class GameWindow(QWidget):
    def __init__(self):
        super().__init__()
        # 获取屏幕参数
        self.screen_size: tuple = get_screen_info()
        self.user_info: dict = pda.load_user_data(data_class.file_user)
        # 背景
        self.widget_bg = WidgetBackground(self)
        # 角色&表情
        self.widget_roles = QWidget(self)
        # 主窗口组件
        self.widget_communication = WidgetCommunication(self)
        # ESC菜单
        self.widget_esc = WidgetEsc(self)
        # 登录界面
        self.widget_login = WidgetLogin(self)

        # 初始化
        self.setup_ui()
        self.init_widgets()

    def go_login_widget(self) -> None:
        # 保存数据 暂停游戏

        # 禁用相关组件
        self.widget_esc.isUsing = False
        self.widget_esc.hide()
        self.widget_esc.toggle_menu()
        self.widget_communication.hide()
        self.widget_login.show()

    def continue_game(self) -> None:
        # 保存数据

        # 隐藏/显示 ESC菜单
        self.widget_esc.toggle_menu()
        # 继续/暂停 游戏进度

    def start_continue_game(self) -> None:
        # 读取数据

        # 显示到游戏进度

        # 切换界面
        self.widget_esc.isUsing = True
        self.widget_esc.show()
        self.widget_communication.show()
        self.widget_bg.show()
        self.widget_roles.show()
        self.widget_login.hide()

    def init_widgets(self, x: int = None, y: int = None) -> None:
        if not x and not y:
            x, y = self.screen_size
        self.widget_bg.init_ui(x, y)
        self.widget_communication.init_dialog_btn(x, y)
        self.widget_esc.init_ui(x, y)
        self.widget_login.init_ui(x, y)

        # 继续游戏-ESC菜单
        self.widget_communication.btn_menu.clicked.connect(self.continue_game)
        # 退出游戏
        self.widget_esc.btn_quit.clicked.connect(self.quit)
        self.widget_login.btn_quit.clicked.connect(self.quit)
        # 回到登录界面
        self.widget_esc.btn_login.clicked.connect(self.go_login_widget)
        # 继续游戏-登录界面
        self.widget_login.btn_continue.clicked.connect(self.start_continue_game)

        self.widget_bg.hide()
        self.widget_communication.hide()

    # 初始化窗口
    def setup_ui(self) -> None:
        self.setGeometry(0, 0, *self.screen_size)
        self.setWindowTitle(self.user_info.get("name"))
        self.setWindowFlag(Qt.WindowType.FramelessWindowHint)

    def keyPressEvent(self, event):
        if event.key() == Qt.Key.Key_Escape:
            self.continue_game()
        else:
            super().keyPressEvent(event)

    def quit(self) -> None:
        # 记得保存数据

        # 摧毁窗口
        self.destroy()
        # 退出程序
        _app = QApplication.instance()
        _app.quit()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    # a = DataChanger()
    # a.show()
    # print(get_screen_info())
    b = GameWindow()
    b.show()
    b.widget_bg.show()
    # 设置背景
    b.widget_bg.set_bg(phot_data.get("bg_test"))  # 使用测试用背景
    b.widget_bg.set_logo(phot_data.get("logo_test"))
    b.widget_communication.show()
    # b.widget_login.show()
    b.widget_esc.isUsing = True
    b.widget_esc.show()
    sys.exit(app.exec())
