from models import Processor
from datetime import datetime


proc = Processor(config="rc_server.yml")

templates = proc.get_templates()
for template in templates:
    print(template)

# Получаем имя для директории с архивами
# name = datetime.now().strftime("%H_%M_%S")
name = "2359"
print(f"dir name: {name}")

# Получаем нужные шаблоны
all_selected_templates = ["СКУО (лок).txt"]

# Ищем готовые архивы
all_ready_archives = proc.get_matches(*all_selected_templates)
print(all_ready_archives)

# Получаем шаблоны, по которым надо сделать архивы
selected_templates = all_selected_templates
# И пути до архивов, которые нужно перенести
ready_archives = []

# Создаем архивы
proc.build_target_dir(name, *selected_templates)

# Добавляем существующие архивы
proc.add_exists_arhive(dir_name=name, *ready_archives)
