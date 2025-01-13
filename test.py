from zipfile import ZipFile, ZIP_DEFLATED
from pathlib import Path, PurePath

# Папка с шаблонами
TEMPLATES = Path("templates")
# Папка с базами
DATA = Path("databases")
# Конечная папку
TARGET = Path("results")


archive_path = Path("results/1212/db.zip")

file = Path("databases")

with ZipFile(archive_path, mode="w", compression=ZIP_DEFLATED,
    allowZip64=True) as myzip:
        myzip.write(file.absolute())
