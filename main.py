from models import ResultsFolder, ArchiveProcessor, YamlHandler, FoldChecker, Options
from pathlib import Path


def txt_del(value: str):
    """Обрезает .txt в конце строки (если есть)"""
    if value[-4:] == ".txt":
        value = value[:-4]
    return value


class Facade:
    def __init__(self):
        self._rc_handler = YamlHandler("rc_server.yml")
        self._options_handler = YamlHandler("options.yml")

    def ready(self):
        # Считываем running config
        self.read_rc_config()
        # Определяем директорию с архивами
        self._archives_dir = ResultsFolder(self.options.archives_path)

    def run(self):
        # Считываем options
        self.read_options_config()
        # Создаем архивы по шаблонам
        templates = self.options.templates
        self.create_archives(*templates)

    def _load_config(self, value):
        value.load_data()
        return value.data

    def get_templates(self):
        templates_checker = FoldChecker(self.options.templates_path)
        return templates_checker.get_all_items_name()

    def read_rc_config(self):
        # Загрузить rc.yml
        data = self._load_config(self._rc_handler)
        # Считать конфигурацию
        templates_path = Path(data["templates"])
        data_path = Path(data["data"])
        archives_path = Path(data["target"])
        # Загрузить конфигурацию в настройки
        self.options = Options(data_path, templates_path, archives_path)
        
    def read_options_config(self):
        # Загрузить options.yml
        data = self._load_config(self._options_handler)
        # Считать конфигурацию и загрузить в настройки
        self.options.folder_name = data["folder name"]
        self.options.compression = data["compression"]
        self.options.templates = data["templates list"]

    def create_archives(self, *templates):
        # Создаем папку в которую поместим архивы
        name = self.options.folder_name
        self._archives_dir.create_sub_folder(name=name)

        # Создадим архивы по шаблонам
        processor = ArchiveProcessor(templates_path=self.options.templates_path,
                                      target_path=self._archives_dir.path_sub_folder,
                                      data_path=self.options.data_path,
                                      compression=self.options.compression)
        processor.create_archives_by_templates(*templates)


if __name__ == "__main__":
    f = Facade()
    f.ready()
    f.run()
