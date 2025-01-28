from main import Facade
import npyscreen as np

COMPRESSIONS = [
    "ZIP_DEFLATED",
    "ZIP_BZIP2",
    "ZIP_LZMA",
    "ZIP_STORED"
]

class MyApp(np.NPSAppManaged):
    def onStart(self):
        self.interface = Facade()
        self.interface.ready()
        self.addForm("MAIN", MainForm)

    def build_archive(self, *templates, **opts):
        self.interface.options.folder_name = opts["folder_name"]
        self.interface.options.compression = opts["compression"]
        self.interface.create_archives(*templates)

# This form class defines the display that will be presented to the user.

class MainForm(np.ActionForm):
    def create(self):
        templates = self.parentApp.interface.get_templates()
        self.folder_name = self.add(np.TitleText,
                                     name = "Folder name:",
                                     value= "")

        self.compression = self.add(np.TitleSelectOne,
                                    max_height=4,
                                    name = "Compression",
                                    values=COMPRESSIONS)

        self.templates = self.add(np.TitleMultiSelect,
                                   name = "Templates:",
                                   values=templates)

    def on_ok(self):
        # Создать архив
        self.parentApp.build_archive(
            folder_name = self.folder_name.value,
            compression = self.compression.get_selected_objects()[0],
            *self.templates.get_selected_objects())

    def on_cancel(self):
        pass

    def afterEditing(self):
        self.parentApp.setNextForm(None)

if __name__ == '__main__':
    TA = MyApp()
    TA.run()
