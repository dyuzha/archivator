from models import ResultsFolder, TemplateProcessor, YamlHandler
from pathlib import Path

yml_handler = YamlHandler("config.yml")
yml_handler.load_data()

paths = yml_handler.data["paths"]
folder_name = yml_handler.data["folder name"]
templates = yml_handler.data["templates list"]

TEMPLATES = Path(paths["templates"])
DATA = Path(paths["data"])
ARCHIVES_DATA = Path(paths["target"])


def main():
    results_folder = ResultsFolder(ARCHIVES_DATA)
    results_folder.create_folder(folder_name)

    processor = TemplateProcessor ( 
        templates_folder=TEMPLATES,
        data_folder=DATA,
        target_folder=results_folder.path_folder
    )

    processor.archive_by_templates(templates)


if __name__ == "__main__":
    main()
