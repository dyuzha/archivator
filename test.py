from zipfile import ZipFile, ZIP_DEFLATED
from pathlib import Path, PurePath

# Папка с шаблонами
TEMPLATES = Path("templates")
# Папка с базами
DATA = Path("databases")
# Конечная папку
TARGET = Path("results")


archive_path = TARGET / "1212/db.zip"

target = Path("databases")

with ZipFile("databases.zip", mode="a") as archive:
    for file_path in target.rglob("*"):
        archive.write(file_path, arcname=file_path.relative_to(target))
        
