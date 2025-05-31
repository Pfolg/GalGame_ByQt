# -*- coding: UTF-8 -*-
"""
PROJECT_NAME GalGameStart
PRODUCT_NAME PyCharm
NAME load_data
AUTHOR Pfolg
TIME 2025/5/28 22:09
"""
# 用来读取用户信息的模块
import os
import socket
import sys

import manage_data as mda
import process_data as pda

DATA = mda.ManageData()


# 获取数据并保存
def data_get_save(**kwargs) -> None:
    if not os.path.exists(DATA.file_user):
        # 判断路径是否存在，不存在则创建
        if not os.path.exists(DATA.folder_user):
            os.mkdir(DATA.folder_user)
        model = DATA.get_metadata()
    else:
        model = pda.load_user_data(DATA.file_user)
    print("储存用户信息的文件路径：", DATA.file_user)

    # 根据输入的信息写入数据
    for key, value in kwargs.items():
        if key not in model.keys():
            continue
        if value is None:
            continue
        model[key] = value
    print("写入数据：【", model, "】\n到文件：【", DATA.file_user, "】")
    pda.save_user_data(DATA.file_user, model)


def load_data() -> dict:
    # 判断文件是否存在
    if not os.path.exists(DATA.file_user):
        return {}
    else:
        return pda.load_user_data(DATA.file_user)


def single_instance(port: int = DATA.metadata.port):
    try:
        # 创建实例，绑定端口
        instance = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        instance.bind(("127.0.0.1", port))
    except socket.error:
        print("另一个实例正在运行，退出。")
        sys.exit(1)
    return instance


if __name__ == '__main__':
    # print(DATA.ui_dir, type(DATA.ui_dir), DATA.ui_manifest.parent, DATA.ui_manifest)
    # create_manifest(DATA.ui_manifest)
    # 创建所有的清单文件
    # DATA.create_all_manifest()
    data_get_save(user=pda.get_user_name(), website="https://www.example.com")
    print("将投入使用的数据：", load_data() if load_data() else "字典为空")
    si = single_instance()
    print("实例状态：", str(si))
