from zipfile import ZipFile, ZIP_DEFLATED, ZIP_BZIP2, ZIP_LZMA, ZIP_STORED
from shutil import copy
from pathlib import Path
from loguru import logger
from os import stat
import yaml
from abc import ABC, abstractmethod
from typing import List, Iterator, Tuple


class ArchiveBuilder(ABC):
    @abstractmethod
    def build_archive(self, *args, **kwargs):
        pass


class Items(Tuple):
    _items: Tuple[Path]

    def __init__(self, values):
        super().__init__()
        if all(isinstance(value, Path) for value in values):
            self._items = values
        else:
            raise ValueError("Значения должны быть экземплярами Path")

    @property
    def name(self) -> Iterator[str]:
        return (item.name for item in self._items)


class YamlHandler:
    def __init__(self, file):
        if not isinstance(file, Path):
            file = Path(file)
        self.file = file
        self.data: dict = {}

    def load_data(self):
        with open(self.file, 'r') as f:
            self.data = yaml.load(f, Loader=yaml.FullLoader)

    def dump_data(self):
        with open(self.file, 'w') as f:
            yaml.dump(self.data, f, default_flow_style=False)

    def get_value(self, key):
        if self.data is not None:
            return self.data[key]
        else:
            return None


class CompressionFactory:
    def create_compression(self, value):
        match value:
            case "ZIP_DEFLATED":
                compression = ZIP_DEFLATED
            case "ZIP_BZIP2":
                compression = ZIP_BZIP2
            case "ZIP_LZMA":
                compression = ZIP_LZMA
            case "ZIP_STORED":
                compression = ZIP_STORED
            case _:
                raise ValueError("Данное значение {} не поддерживается".format(value))
        return compression


class ZipArchiveBuilder(ArchiveBuilder):
    _compression = ZIP_DEFLATED

    def __init__(self):
        logger.debug("ZipArchiveBuilder конструктор вызван с параметром \
compression = {}".format(self._compression))

    @property
    def compression(self):
        return self._compression

    @compression.setter
    def compression(self, value):
        factory = CompressionFactory()
        self._compression = factory.create_compression(value)

    def build_archive(self, archive: Path, *items):
        for item in items:
            self._recurcieve_add_to_archive(archive, item)
            logger.info(f"Архив {archive.name} построен")

    def _recurcieve_add_to_archive(self, archive: Path, item: Path, indent_dir=""):
        # Добавляем item в архив
        with ZipFile(archive, mode="a", compression=self._compression,
                     allowZip64=True) as zf:
            zf.write(item, arcname=indent_dir + item.name)
            logger.debug(f"{item.name} добавлен в архив {archive.name}")

        # Если item является директорией, то все содержимое добавляем в архив
        if item.is_dir():
            dir = item
            indent_dir += dir.name + "/"
            for indent_item in dir.iterdir():
                self._recurcieve_add_to_archive(archive, indent_item,
                                               indent_dir=indent_dir)
            logger.debug(f"Директория {dir.name} добавлена в архив {archive.name}")


class DefaultFolder():
    # Переменная для отслеживания единственности экземпляра
    _instance = None

    _path: Path
    _items: Items

    def __init__(self, path):
        if isinstance(path, str):
            path = Path(path)
        if not path.is_dir():
            raise ValueError("Указанный файл {} должен быть \
директорией".format(path))
        self._path = path
        self.load_items()


    @classmethod
    # Действия при создании нового экземпляра класса
    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            # Создается новый экземпляр в переменную класса
            cls._instance = super().__new__(cls)
        # Возвращается экземпляр хранящийся в переменной класса
        return cls._instance

    @property
    def path(self):
        return self._path

    @property
    def items(self):
        return self._items

    def load_items(self):
        items = tuple(self._path.iterdir())
        self._items = Items(items)


class Templates(DefaultFolder):
    _path: Path
    _items: Items

    @staticmethod
    def name_handle(value):
        if value[-1:] == "\\" or "\n":
            Templates.name_handle(value[:-1])
        return value

    def get_content(self, template: str):
        file = self.path / Path(template)
        content = []
        with open(file, "r") as f:
            for line in f.readlines():
                handler_line = Templates.name_handle(line)
                content.append(handler_line)
        return content


class ArchiveProcessor(DefaultFolder):
    _archive_builder = ZipArchiveBuilder

    def build_archive(self, archive, *items):
        self._archive_builder.build_archive(archive, *items)

    def get_matches(self, *names) -> List:
        """Находит совпадающие архивы по названиям, возвращает список найденных архивов"""
        self.load_items()
        matches = []
        for item in self.items:
            for value in names:
                if item.name == value:
                    matches.append(item)
        return matches

    def mksubdir(self, name):
        path = self.path / name
        path.mkdir(exist_ok=True)
        logger.info(f"Создана папка {path.name}")
        # Обновляем информацию о директориях
        self.load_items()

    def delete_dir(self, name):
        pass


class Processor:
    _ap: ArchiveProcessor
    _templates: Templates
    _data: DefaultFolder


    def __init__(self, config):
        self._config = YamlHandler(config)
        self.read_config()

    def read_config(self):
        self._config.load_data()
        self._ap = ArchiveProcessor(self._config.data["archives"])
        self._templates = Templates(self._config.data["templates"])
        self._data = DefaultFolder(self._config.data["data"])

    def get_templates(self):
        return self._templates.items.name

    def get_matches(self, *value):
        return self._ap.get_matches(*value)

    def build_target_dir(self, dir_name, *templates):
        self._ap.mksubdir(dir_name)
        for template in templates:
            archive = self._ap.path / dir_name / template
            self._build_archive(archive, template)

    def add_exists_arhive(self, dir_name, *archives):
        dir = Path(self._ap.path / Path(dir_name))
        for archive in archives:
            copy(archive, dir)

    def _build_archive(self, archive, template):
        file_names = self._templates.get_content(template)
        for file_name in file_names:
            file_path = self._data.path / Path(file_name)
            self._ap.build_archive(archive, file_path)
