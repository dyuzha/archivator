from zipfile import ZipFile, ZIP_DEFLATED
from pathlib import Path, PurePath
from loguru import logger
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


    def add_to_archive(self, zip_file, file):
        """
        Добавляет рекурсивно файл(ы) в архив
        :param zip_file: Zip-файл, который необходимо дополнить файлом
        :param folder_path: Путь к файлу для рекурсивного добавления
        """
        with ZipFile(zip_file, mode="a", compression=self.compression,
                        allowZip64=self.allow_zip64) as archive:
            for file in Path(file).iterdir():
                if file.is_file():
                    archive.write(file, arcname=file.name)
                    logger.debug(f"Файл {file.name} добавлен в архив {zip_file.name}")
                elif file.is_dir():
                    # Рекурсивный вызов для обработки подпапок
                    archive.write(file, arcname=file.name)
                    self.add_to_archive(archive, file)
                    logger.debug(f"Папка {file.name} добавлена в архив {zip_file.name}")



class ResultsFolder(object):
    # Переменная для отслеживания единственности экземпляра
    instance = None

    # Действия при создании нового экземпляра класса
    def __new__(cls, *args, **kwargs):
        if not cls.instance:
            # Создается новый экземпляр в переменную класса
            cls.instance = super().__new__(cls)
        # Возвращается экземпляр хранящийся в переменной класса
        return cls.instance

    def create_folder(self, name):
        self.path = Path(TARGET / Path(name))
        # Проверяем, существует ли папка
        if not self.path.exists():
            # Если папка не существует, создаем ее
            self.path.mkdir()
            logger.info(f"Создана папка {self.path.name}")


class TemplateProcessor(object):
    def __init__(self, target_folder: PurePath):
        self.target_folder = target_folder

    def archive_by_templates(self, templates) -> None:
        for template in templates:
            archive_path = Path(self.target_folder / Path(template + ".zip"))
            databases = self.get_databases(template)
            self.create_archive(databases, archive_path)

    def get_databases(self, template) -> list:
        """Получает список информационных баз из шаблона"""
        databases = list()
        with open(Path(TEMPLATES / template), 'r') as file:
            for line in file.readlines():
                line = line[:-1]
                databases.append(line)
        return databases

    def create_archive(self, databases, archive_path) -> None:
        builder = ZipArchiveBuilder()
        files_pathes = list()
        for db_name in databases:
            file_path = Path(DATA / Path(db_name))
            files_pathes.append(file_path)
        builder.build_archive(archive_path, *files_pathes)


# Папка с шаблонами
TEMPLATES = Path("templates")
# Папка с базами
DATA = Path("databases")
# Конечная папку
TARGET = Path("results")


folder_name = "1212"

def main():
    results_folder = ResultsFolder()
    results_folder.create_folder(folder_name)

    processor = TemplateProcessor(results_folder.path)
    processor.archive_by_templates(["pat_1", "pat_3"])


if __name__ == "__main__":
    main()
