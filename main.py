from models import Processor
from datetime import datetime


proc = Processor(config="rc.yml")

templates = proc.get_templates()
for template in templates:
    print(template)

# Получаем имя для директории с архивами
name = str(datetime.now().time())
print(f"dir name: {name}")

# Получаем нужные шаблоны
all_selected_templates = ["pat_1", "pat_2"]

# Ищем готовые архивы
all_ready_archives = proc.get_matches(*all_selected_templates)
print(all_ready_archives)

# Получаем шаблоны, по которым надо сделать архивы
selected_templates = all_selected_templates
# И пути до архивов, которые нужно перенести
ready_archives = []

# Создаем архивы
proc.build_target_dir(dir_name=name, *selected_templates)

# Добавляем существующие архивы
print(datetime.now().time())
proc.add_exists_arhive(dir_name=name, *ready_archives)
