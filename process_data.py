# -*- coding: UTF-8 -*-
"""
PROJECT_NAME GalGameStart
PRODUCT_NAME PyCharm
NAME process_data
AUTHOR Pfolg
TIME 2025/5/27 13:00
"""
# [基础]用来保存/读取数据到文件的模块
import base64
import os
import pickle
import platform

from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
from base64 import b64encode
import getpass
import hashlib

from PySide6.QtGui import QFontDatabase


# 替换数字
def replace_num(inp: str):
    converts = {
        "1": "一",
        "2": "二",
        "3": "三",
        "4": "四",
        "5": "五",
        "6": "六",
        "7": "七",
        "8": "八",
        "9": "九",
        "0": "零",
    }
    out = ""
    for i in inp:
        if converts.get(i):
            out += converts[i]
        else:
            out += i
    return out


# 获取用户名
def get_user_name():
    return getpass.getuser() or "unknown_user"


# 电脑名
def get_computer_name():
    return platform.node() or "unknown_host"


def make_key():
    # 使用 getpass 模块获取用户名
    username_getpass = getpass.getuser() or "unknown_user"
    # 获取电脑名
    computer_name = platform.node() or "unknown_host"

    name = f"{username_getpass}_{computer_name}"
    # 替换数字+大写+编码+sha256加密+32字节化
    header = hashlib.sha256(replace_num(name).upper().encode('utf-8')).digest()

    return hashlib.sha256(name.encode()).digest(), header  # 密钥+文件头


# 加密
def encrypt_data(data, key, header):
    # 序列化数据
    serialized = pickle.dumps(data)

    # 初始化加密器
    cipher = AES.new(key, AES.MODE_CBC)
    ct_bytes = cipher.encrypt(pad(serialized, AES.block_size))

    # 组合 IV + 密文
    encrypted_data = cipher.iv + ct_bytes

    # Base64 编码 + 添加混淆头
    final_data = header + b"%%SEP%%" + b64encode(encrypted_data)
    return final_data


# 解密
def decrypt_data(encrypted_data, key, header):
    try:
        # --- 步骤 1：分割混淆头和数据 ---
        separator = b"%%SEP%%"
        header_part, sep, data_part = encrypted_data.partition(separator)

        if not sep:
            raise ValueError("无效文件格式：未找到分隔符")

        # --- 步骤 2：验证混淆头 ---
        expected_header = header
        if header_part != expected_header:
            raise PermissionError("文件头不匹配：可能来自其他设备或用户")

        # --- 步骤 3：Base64 解码 ---
        decoded_data = base64.b64decode(data_part)

        # --- 步骤 4：提取 IV 和密文 ---
        # 注意：IV 长度需与加密时的 AES.block_size 一致（通常 16 字节）
        iv = decoded_data[:AES.block_size]
        ct = decoded_data[AES.block_size:]

        # --- 步骤 5：解密数据 ---
        cipher = AES.new(key, AES.MODE_CBC, iv)
        pt = unpad(cipher.decrypt(ct), AES.block_size)

        # --- 步骤 6：反序列化 ---
        return pickle.loads(pt)

    except (ValueError, KeyError) as e:
        # 处理 Padding/格式错误
        raise RuntimeError("解密失败：数据可能被篡改") from e
    except Exception as e:
        # 捕获其他意外错误
        raise RuntimeError(f"解密过程异常: {str(e)}") from e


# 保存与加载加密文件
def save_user_data(file_path, data, k=make_key()[0], h=make_key()[1]):
    encrypted = encrypt_data(data, key=k, header=h)
    with open(file_path, 'wb') as f:
        f.write(encrypted)


def load_user_data(file_path, k=make_key()[0], h=make_key()[1]):
    if os.path.exists(file_path):
        with open(file_path, 'rb') as f:
            encrypted = f.read()
        return decrypt_data(encrypted, key=k, header=h)
    else:
        raise FileNotFoundError(f"未找到文件 <{file_path}>")


def load_font(path: str) -> str:
    # 设置字体
    font_id = QFontDatabase.addApplicationFont(path)
    if font_id == -1:
        print("字体加载失败！")
        # 处理加载失败情况
        font_family = "Ubuntu Mono"
    else:
        # 2. 获取字体家族名称
        font_families = QFontDatabase.applicationFontFamilies(font_id)
        if font_families:
            font_family = font_families[0]  # 通常第一个就是我们要的
            print(f"成功加载字体: {font_family}")
        else:
            font_family = "Ubuntu Mono"

    return font_family


if __name__ == '__main__':
    print(make_key())
    data_file = "test.dat"
    test_data = {
        "数据1": "123",
        "数据2": "Python",
        "数据3": "Password",
    }
    save_user_data(data_file, test_data)
    print(load_user_data(data_file))
