from zipfile import ZipFile, ZIP_DEFLATED, ZIP_BZIP2, ZIP_LZMA, ZIP_STORED
from pathlib import Path
from loguru import logger
import yaml
from abc import ABC, abstractmethod

def back_slash_del(value: str):
    """Обрезает \\ в конце строки (если есть)"""
    if value[-1:] == "\\":
        value = value[:-1]
    return value


class Options(object):
    def __init__(self, data_path, templates_path, archives_path,  
                 *templates, **opts):
        self.data_path = data_path
        self.templates_path = templates_path
        self.archives_path = archives_path

        self.folder_name = opts.get("folder_name", None)
        self.compression = opts.get("compression", 0)

        self.templates = templates

    @property
    def compression(self):
        return self._compression
    
    @compression.setter
    def compression(self, value):
        if isinstance(value, int):
            self._compression = value
        else:
            match value:
                case "ZIP_DEFLATED":
                    self._compression = ZIP_DEFLATED
                case "ZIP_BZIP2":
                    self._compression = ZIP_BZIP2
                case "ZIP_LZMA":
                    self._compression = ZIP_LZMA
                case "ZIP_STORED":
                    self._compression = ZIP_STORED
                case _:
                    raise ValueError("Данное значение {} не поддерживается".format(value))


class ArchiveBuilder(ABC):
    @abstractmethod
    def build_archive(self, *args, **kwargs):
        pass


class ZipArchiveBuilder(ArchiveBuilder):
    def __init__(self, compression=ZIP_DEFLATED):
        self.compression = compression
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
                     allowZip64=True) as zf:
            try:
                zf.write(file, arcname=indent_dir + file.name)
                logger.debug(f"Файл {file.name} добавлен в архив {zip_file.name}")
            except Exception as ex:
                logger.critical(f"[WARN]: Файл {file.name} не добавлен в архив {zip_file.name}, {ex}")


        if file.is_dir():
            dir: Path = file
            indent_dir += dir.name + "/"
            for indent_file in dir.iterdir():
                self.recurcieve_add_to_archive(zip_file, indent_file, indent_dir=indent_dir)
            logger.debug(f"Папка {dir.name} добавлена в архив {zip_file.name}")


class FoldChecker:
    def __init__(self, dir_path: Path):
        self.dir_path = dir_path
        if not self.dir_path.is_dir():
            raise ValueError("Указанный файл {} должен быть директорией".format(dir_path))

    def get_all_items(self) -> list:
        """Возрвращает список всех элементов в директории"""
        return [item for item in self.dir_path.iterdir()]

    def get_all_items_name(self) -> list:
        """Возрвращает список имен всех элементов в директории"""
        return [item.name for item in self.dir_path.iterdir()]

    def _get_all_indent_items(self, items: list):
        """Возвращает список элементов во вложенных папках"""
        indent_items = []
        for item in items:
            if item.is_dir():
                fold_checker = FoldChecker(item)
                indent_items.extend(fold_checker.get_all_items())
        return indent_items

    def get_all_indent_items(self):
        """Удобный интерфейс для получения списка элемнтов во вложенных папках"""
        items = self.get_all_items()
        return self._get_all_indent_items(items)


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

    def get_value(self, key):
        if self.data is not None:
            return self.data[key]
        else:
            return None


class ResultsFolder(object):
    # Переменная для отслеживания единственности экземпляра
    instance = None

    def __init__(self, path: Path):
        self.path = path

    # Действия при создании нового экземпляра класса
    def __new__(cls, *args, **kwargs):
        if not cls.instance:
            # Создается новый экземпляр в переменную класса
            cls.instance = super().__new__(cls)
        # Возвращается экземпляр хранящийся в переменной класса
        return cls.instance

    def create_sub_folder(self, name: str):
        self.path_sub_folder = self.path / Path(name)
        # Проверяем,create_sub_folder существует ли папка
        if not self.path_sub_folder.exists():
            # Если папка не существует, создаем ее
            self.path_sub_folder.mkdir()
            logger.info(f"Создана папка {self.path_sub_folder.name}")


class ArchiveProcessor(object):
    def __init__(self, target_path, templates_path, data_path,
                 compression):
        self.target_folder = target_path
        self.templates_folder = templates_path
        self.data_folder = data_path
        self.compression = compression

    def create_archives_by_templates(self, *templates) -> None:
        try:
            for template in templates:
                archive_path = Path(self.target_folder / Path(template + ".zip"))
                databases = self.get_databases(template)
                self.create_archive(databases=databases, 
                                    archive_path=archive_path, 
                                    compression=self.compression)
            logger.info(f"Директория [{self.target_folder}] сорбрана")

        except Exception as ex:
            logger.critical(f"Директория [{self.target_folder}] не сорбрана.\n [WARN]: {ex}")

    def get_databases(self, template) -> list:
        """Получает список информационных баз из шаблона"""
        databases = list()
        with open(Path(self.templates_folder / template), 'r') as file:
            for line in file.readlines():
                line = line[:-1]
                databases.append(line)
        return databases

    def create_archive(self, databases, archive_path, compression) -> None:
        builder = ZipArchiveBuilder(compression=compression)

        # Удаляем обратный слэш, если есть
        databases = list(map(back_slash_del, databases))

        # Собираем список файлов для архивирования
        files_pathes = list()
        for db_name in databases:
            file_path = Path(self.data_folder / Path(db_name))
            files_pathes.append(file_path)

        builder.build_archive(archive_path, *files_pathes)
