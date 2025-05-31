# -*- coding: UTF-8 -*-
"""
PROJECT_NAME GalGameStart
PRODUCT_NAME PyCharm
NAME asset_data
AUTHOR Pfolg
TIME 2025/5/29 12:06
"""
# 存储文件数据的模块
import manage_data as mda

ex = mda.ManageData()

current_path = ex.current_path

ui_data = {
    "develop": current_path / "assets/ui/develop.ui"
}

phot_data = {
    "bg_test": current_path / "assets/photos/658397c325e34978b818c9870195df9a.jpg",
    "logo_test": current_path / "assets/photos/logo_test.png",
    "btn_head": current_path / "assets/photos/caret-right.svg",
    "btn_back": current_path / "assets/photos/caret-left.svg",
    "btn_menu": current_path / "assets/photos/bars.svg",
    "btn_bookmark": current_path / "assets/photos/bookmark.svg",
    "btn_automatic_play": current_path / "assets/photos/circle-play.svg",
    "btn_automatic_stop": current_path / "assets/photos/circle-pause.svg",
}
text_data = {}
voice_data = {}
font_data = {
    "MapleMono-NF-CN-Medium": current_path / "assets/font/MapleMono-NF-CN-Medium.ttf"
}


# 写入数据
def update_data():
    mda.write_manifest(ex.ui_manifest, ui_data)
    mda.write_manifest(ex.phot_manifest, phot_data)
    mda.write_manifest(ex.text_manifest, text_data)
    mda.write_manifest(ex.voice_manifest, voice_data)
    mda.write_manifest(ex.font_manifest, font_data)


if __name__ == '__main__':
    update_data()
