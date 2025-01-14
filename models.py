from zipfile import ZipFile, ZIP_DEFLATED
from pathlib import Path, PurePath
from loguru import logger
import yaml
from abc import ABC, abstractmethod


class ArchiveBuilder(ABC):
    @abstractmethod
    def build_archive(self, *args, **kwargs):
        pass


class ZipArchiveBuilder(ArchiveBuilder):
    def __init__(self, compression=ZIP_DEFLATED, allow_zip64=True):
        self.compression = compression
        self.allow_zip64 = allow_zip64
        logger.debug("Конструктор вызван")

    def build_archive(self, archive_path: Path,  *files_pathes):
        for file_path in files_pathes:
            self.recurcieve_add_to_archive(archive_path, file_path)
        logger.info(f"Архив {archive_path.name} построен")

    def recurcieve_add_to_archive(self, zip_file: Path, file: Path, indent_dir=""):
        """
        Добавляет рекурсивно файл в архив
        :param zip_file: Path, Zip-файл, который необходимо дополнить файлом
        :param file: Path, Путь к файлу для рекурсивного добавления
        :param indent_dir: str, показывает в какую папку в архиве необходимо
        поместить файл
        """
        with ZipFile(zip_file, mode="a", compression=self.compression,
                     allowZip64=self.allow_zip64) as zf:
            zf.write(file, arcname=indent_dir + file.name)
            logger.debug(f"Файл {file.name} добавлен в архив {zip_file.name}")

        if file.is_dir():
            dir: Path = file
            indent_dir += dir.name + "/"
            for indent_file in dir.iterdir():
                self.recurcieve_add_to_archive(zip_file, indent_file, indent_dir=indent_dir)
            logger.debug(f"Папка {dir.name} добавлена в архив {zip_file.name}")


class YamlHandler:
    def __init__(self, file_path):
        self.file_path = file_path
        self.data: dict = {}

    def load_data(self):
        with open(self.file_path, 'r') as file:
            self.data = yaml.load(file, Loader=yaml.FullLoader)

    def dump_data(self):
        with open(self.file_path, 'w') as file:
            yaml.dump(self.data, file, default_flow_style=False)



class ResultsFolder(object):
    def __init__(self, path: Path):
        self.path = path
    # Переменная для отслеживания единственности экземпляра
    instance = None

    # Действия при создании нового экземпляра класса
    def __new__(cls, *args, **kwargs):
        if not cls.instance:
            # Создается новый экземпляр в переменную класса
            cls.instance = super().__new__(cls)
        # Возвращается экземпляр хранящийся в переменной класса
        return cls.instance

    def create_folder(self, name: str):
        self.path_folder = self.path / Path(name)
        # Проверяем, существует ли папка
        if not self.path_folder.exists():
            # Если папка не существует, создаем ее
            self.path_folder.mkdir()
            logger.info(f"Создана папка {self.path.name}")


class TemplateProcessor(object):
    def __init__(self, target_folder, templates_folder, data_folder):
        self.target_folder = target_folder
        self.templates_folder = templates_folder
        self.data_folder = data_folder

    def archive_by_templates(self, templates) -> None:
        for template in templates:
            archive_path = Path(self.target_folder / Path(template + ".zip"))
            databases = self.get_databases(template)
            self.create_archive(databases, archive_path)

    def get_databases(self, template) -> list:
        """Получает список информационных баз из шаблона"""
        databases = list()
        with open(Path(self.templates_folder / template), 'r') as file:
            for line in file.readlines():
                line = line[:-1]
                databases.append(line)
        return databases

    def create_archive(self, databases, archive_path) -> None:
        builder = ZipArchiveBuilder()
        files_pathes = list()
        for db_name in databases:
            file_path = Path(self.data_folder / Path(db_name))
            files_pathes.append(file_path)
        builder.build_archive(archive_path, *files_pathes)
