from models import ResultsFolder, TemplateProcessor, YamlHandler, FoldChecker
from pathlib import Path


class Facade:
    def __init__(self):
        self.rc_handler = YamlHandler("rc.yml")
        self.options_handler = YamlHandler("options.yml")

    def load_config(self, value):
        value.load_data()
        return value.data

    def get_options(self, folder_name:str, compression:str, allow_zip64=True, *templates):
        self.folder_name = folder_name
        self.compression = compression
        self.allow_zip64 = allow_zip64
        self.templates = templates
        print(self.compression)

    def get_selected_templates(self):
        # Получить список шаблонов
        self.templates_checker = FoldChecker(self.templates_folder)
        return self.templates_checker.get_all_items()
    

    def read_rc_config(self):
        # Загрузить rc.yml
        data = self.load_config(self.rc_handler)

        # Считать конфигурацию
        self.templates_folder = Path(data["templates"])
        self.data_folder = Path(data["data"])
        self.results_folder = ResultsFolder(Path(data["target"]))
        
    def read_options_config(self):
        # Загрузить options.yml
        data = self.load_config(self.options_handler)

        # Считать конфигурацию
        self.get_options(
            data["folder name"], data["compression"], 
            data["allow_zip64"], *data["templates list"]
            )

    def create_archives_by_templates(self, *templates):
        # Создадим результирующую папку
        self.results_folder.create_folder(self.folder_name)

        # Создадим архивы по шаблонам
        processor = TemplateProcessor(templates_folder=self.templates_folder,
                                      target_folder=self.results_folder.path_folder,
                                      data_folder=self.data_folder,
                                      compression=self.compression,
                                      allow_zip64=self.allow_zip64
                                      )
        processor.create_archives_by_templates(templates)

    def create_archives_by_selected_templates(self):
        self.create_archives_by_templates(*self.templates)


if __name__ == "__main__":
    f = Facade()
    f.read_rc_config()
    f.read_options_config()
    f.create_archives_by_selected_templates()
