from zipfile import ZipFile


def archive_file(src, target_folder):
    file_name = target_folder "/" + src + ".zip"
    with ZipFile(file_name, mode="w", compression=ZIP_DEFLATED, allowZip64=True) as myzip:
        myzip.write(src)


data_path = "databases"
templates_path = "templates"
target_path = "results"
mode_app = "create" # | ""


application_number = "123"

target_folder = target_path + application_number

# Создает папку
create(target_folder)

for file in templates_path:
    try:
        archive_file(file, target_path)
    except Exception as e:
        return "При обработки файла произошла ошибка: {}, {}".format(src, e)
    else:
        return "Файл {} успешно архивировался".format(src)
