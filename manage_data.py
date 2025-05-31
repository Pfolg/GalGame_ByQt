# -*- coding: UTF-8 -*-
"""
PROJECT_NAME GalGameStart
PRODUCT_NAME PyCharm
NAME manage_data
AUTHOR Pfolg
TIME 2025/5/27 18:47
"""
# [基础]用来生成初始数据的模块
import json
import os.path
import pathlib
from pathlib import Path
from dataclasses import asdict, dataclass
from typing import List, Optional


def get_book_mark_example() -> dict:
    # 记得在使用数据时进行排序
    return {
        "latest": "0,0,0",  # 根据剧本拟定格式
        "other": [],
    }


@dataclass
class ProjectMetadata:
    authors: List[str]
    version: str
    port: int
    description: Optional[str] = None  # 使用Optional明确可为None
    name: Optional[str] = None
    nickname: Optional[str] = None
    website: Optional[str] = None
    speed: Optional[int] = None
    user: Optional[str] = None
    latest_point: Optional[str] = None


class ManageData:
    def __init__(self):
        # 基本信息
        self.metadata = ProjectMetadata(
            authors=["Pfolg"],
            version="v1.0.0",
            port=25529,
            latest_point="0",
            description=None,
            name=None,
            website=None,
            speed=10,
            user=None,
        )
        # 文件信息
        self.current_path = Path.cwd()
        self.folder_user = self.current_path / "user_data"
        self.file_user = self.folder_user / "user_data.dat"
        self.file_bookmark = self.folder_user / "bookmark.dat"
        # 内容管理
        self.assets_root = self.current_path / "assets"  # 资源根目录
        # 资源类型配置 (资源类型名: (子目录名, 清单文件名))
        self.resource_types = {
            "phot": ("photos", "manifest.json"),
            "voice": ("voice", "manifest.json"),
            "text": ("text", "manifest.json"),
            "ui": ("ui", "manifest.json"),
            "font": ("font", "manifest.json"),
        }
        # 收集路径到file_manager
        self.file_manager = {
            "root": [],
            "manifest": []
        }

        # 动态生成路径属性
        self._path_attrs = []  # 存储所有路径属性名
        for res_type, (sub_dir, manifest_file) in self.resource_types.items():
            # 生成目录路径（如 phot_dir）
            # 访问：ManageData.phot_dir
            dir_attr = f"{res_type}_dir"
            setattr(self, dir_attr, self.assets_root / sub_dir)
            self._path_attrs.append(Path(dir_attr))
            self.file_manager["root"].append(getattr(self, dir_attr))

            # 生成清单文件路径（如 phot_manifest）
            # 访问：ManageData.phot_manifest
            manifest_attr = f"{res_type}_manifest"
            setattr(self, manifest_attr, getattr(self, dir_attr) / manifest_file)
            self._path_attrs.append(Path(manifest_attr))
            self.file_manager["manifest"].append(getattr(self, manifest_attr))

    # 创建基本文件夹
    @staticmethod
    def create_dir(_dir: pathlib.Path) -> None:
        if not os.path.exists(_dir):
            os.mkdir(_dir)

    # 创建清单文件
    def create_manifest(self, file: pathlib.Path) -> None:
        self.create_dir(file.parent)
        model = {"root": str(file.parent)}
        with open(file, "w", encoding="utf-8") as f:
            json.dump(model, f, indent=4, ensure_ascii=False)

    # 创建所有清单文件
    def create_all_manifest(self) -> None:
        for i in self.file_manager["manifest"]:
            self.create_manifest(i)

    def update_metadata(self, **kwargs) -> None:
        """动态更新metadata字段，跳过无效字段和空值"""
        # 具体字段请查看该类下的字段：ProjectMetadata
        valid_fields = {f.name for f in ProjectMetadata.__dataclass_fields__.values()}

        for key, value in kwargs.items():
            # 1. 检查是否为有效字段
            if key not in valid_fields:
                continue

            # 2. 跳过空值（按需调整）
            if value is None:
                continue

            # 3. 更新字段值
            setattr(self.metadata, key, value)

    def get_metadata(self):
        return asdict(self.metadata)

    def show_data(self) -> dict:
        print("\n".join(f"{i}:{j}" for i, j in self.metadata.__dict__.items()))
        return asdict(self.metadata)


# 读取清单
def read_manifest(file: pathlib.Path) -> dict:
    if os.path.exists(file):
        with open(file, "r", encoding="utf-8") as f:
            d: dict = json.load(f)
            # 转换为Path
            return convert_value_to_path(d)
    return {"root": file.parent}


# 将字典中的value转换为str
def convert_value_to_str(target: dict[str:pathlib.Path]) -> dict[str:str]:
    return {f"{k}": str(v) for k, v in target.items()}


# 将字典中的value转换为Path
def convert_value_to_path(target: dict[str:str]) -> dict[str:pathlib.Path]:
    return {f"{k}": Path(v) for k, v in target.items()}


# 写入清单
def write_manifest(file: pathlib.Path, data: dict) -> None:
    ManageData.create_dir(file.parent)
    origin = read_manifest(file)
    for k, v in data.items():
        origin[k] = v
    save_data = convert_value_to_str(origin)
    with open(file, "w", encoding="utf-8") as f:
        json.dump(save_data, f, ensure_ascii=False, indent=4)


def write_json_data(file: str, data: dict) -> None:
    path = Path(file)
    ManageData.create_dir(path.parent)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)


def read_json_data(file) -> dict:
    if os.path.exists(file):
        with open(file, "r", encoding="utf-8") as f:
            d: dict = json.load(f)
        return d
    else:
        write_json_data(file, get_book_mark_example())
        return get_book_mark_example()


if __name__ == '__main__':
    t = ManageData()
    t.show_data()
    t.update_metadata(
        authors=["Alice", "Bob"],
        website="https://example.com",
        speed=5,
        description="这是一段测试数据",
        invalid_field="ignored"  # 自动忽略
    )

    print(read_manifest(t.ui_manifest))
    print(t.metadata.authors)
    print(t.resource_types)
