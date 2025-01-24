from models import Processor
import npyscreen
from dataclasses import dataclass

@dataclass
class Options:
    folder_name: str = "Bases"
    selected_templates: list = []


class AllowForm(npyscreen.ActionForm):
    def create(self):
        folder_name = self.add(npyscreen.TitleText,
                                    name = "Folder name:",
                                    value = "")

        self.options = Options(folder_name=folder_name.value)

    def on_ok(self):
        self.parentApp.options = self.options
        self.parentApp.switchForm('TEMPLATES')


class OptionsForm(npyscreen.ActionForm):
    def create(self):
        folder_name = self.add(npyscreen.TitleText,
                                    name = "Folder name:",
                                    value = "")

        self.options = Options(folder_name=folder_name.value)

    def on_ok(self):
        self.parentApp.options = self.options
        self.parentApp.switchForm('TEMPLATES')


class TemplatesForm(npyscreen.ActionForm):
    def create(self):
        templates = list(self.parentApp.processor.get_templates())
        self.selected_templates = self.add(npyscreen.TitleMultiSelect,
                                   name = "Templates:",
                                   values=templates)
    def on_ok(self):
        self.parentApp.options.selected_templates = self.selected_templates
        self.parentApp.switchForm('ALLOW')


class App(npyscreen.NPSAppManaged):
    @property
    def options(self):
        return self._options

    @options.setter
    def options(self, value):
        self._options = value

    def build_dir(self):
        dir_name = self.options.dir_name
        templates = self.options.selected_templates
        self.processor.build_target_dir(dir_name, *templates)

    def onStart(self):
        self.processor = Processor("rc.yml")
        self.addForm("MAIN", OptionsForm, name="Options")
        self.addForm("TEMPLATES", TemplatesForm, name="Templates")
        self.addForm("ALLOW", AllowForm, name="Allow")


if __name__ == '__main__':
    app = App()
    app.run()
