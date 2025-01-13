from zipfile import ZipFile, ZIP_DEFLATED
from pathlib import Path, PurePath
from abc import ABC, abstractmethod


class ArchiveBuilder(ABC):
    @abstractmethod
    def build_archive(self, *args, **kwargs):
        pass


class DefaultArchiveBuilder(ArchiveBuilder):
    def __init__(self, compression=ZIP_DEFLATED, allow_zip64=True):
        self.compression = compression
        self.allow_zip64 = allow_zip64

    def build_archive(self, archive_path: PurePath,  *files):
        # Создание пустого zip архива
        with ZipFile('archive.zip', 'w') as zip_file:
            pass

            for file in files:
            #     for sub_file in file.rglob("*"):
            #         myzip.write(sub_file, arcname=sub_file.relative_to(file))
                self.add_to_archive(archive_path, file)
            #
            # with ZipFile(archive_path, mode="a", compression=self.compression,
            #              allowZip64=self.allow_zip64) as archive:

            

    def add_to_archive(self, zip_file, file_path):
        """
        Добавляет рекурсивно файл(ы) в архив
        :param zip_file: Zip-файл, который необходимо дополнить файлом
        :param folder_path: Путь к файлу для рекурсивного добавления
        """
        with ZipFile(zip_file, mode="a", compression=self.compression,
                        allowZip64=self.allow_zip64) as archive:

            for file in Path(file_path).iterdir():
                if file.is_file():
                    archive.write(file)
                elif file.is_dir():
                    # Рекурсивный вызов для обработки подпапок
                    archive.write(file)
                    self.add_to_archive(archive, file)  



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
        # Проверяем, существует ли папка TARGET / Path(TICKET)
        if not self.path.exists():
            # Если папка не существует, создаем ее
            self.path.mkdir()


class TemplateProcessor(object):
    def __init__(self, target_folder: PurePath):
        self.target_folder = target_folder

    def archive_by_templates(self, templates) -> None:
        for template in templates:
            archive_path = Path(self.target_folder / Path(template + ".zip"))
            databases = self.get_databases(template)
            self.create_archive(databases, archive_path)

    def get_databases(self, template) -> list:
        # Список информационных баз из шаблона
        databases = list()
        with open(Path(TEMPLATES / template), 'r') as file:
            for line in file.readlines():
                line = line[:-1]
                databases.append(line)
        return databases

    def create_archive(self, databases, archive_path) -> None:
        builder = DefaultArchiveBuilder()
        files = list()
        for db_name in databases:
            file = Path(DATA / Path(db_name))
            files.append(file)
        builder.build_archive(archive_path, *files)


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
