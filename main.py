from pathlib import Path
from models import Processor, YamlHandler

config = YamlHandler("rc.yml")
config.load_data()

# Считываем конфиг
archives = config.data["archives"]
templates = config.data["templates"]
data = config.data["data"]

name = "test_dir"

proc = Processor(archives, templates, data)

templates = proc.get_templates()

print(templates)

# proc.build_target_dir(name, *templates)







