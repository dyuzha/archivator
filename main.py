from models import ResultsFolder, TemplateProcessor, YamlHandler
from pathlib import Path


rc_handler = YamlHandler("rc.yml")
rc_handler.load_data()
rc_data = rc_handler.data

TEMPLATES = Path(rc_data["templates"])
DATA = Path(rc_data["data"])
ARCHIVES_DATA = Path(rc_data["target"])

options_handler = YamlHandler("options")
options_handler.load_data()
options_data = options_handler.data

folder_name = options_data["folder name"]
templates = options_data["templates list"]
compression = options_data["compression"]
allow_zip64 = options_data["allow_zip64"]

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
