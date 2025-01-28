from models import Processor
import npyscreen
from dataclasses import dataclass, field


@dataclass
class Options:
    folder_name: str = "Bases"
    selected_templates: list = field(default_factory=list)


class AllowForm(npyscreen.ActionForm):
    def create(self):
        self.show_atx = 20
        self.show_aty = 10

        folder_name = self.add(
                npyscreen.TitleText,
                name = "Folder name:",
                value =self.parentApp.options.folder_name
                )
        # selected_templates = self.add(npyscreen.)

        # self.options = Options(folder_name=folder_name.value)
        # self.options = Options(selected_templates=selected_templates.value)

    def on_ok(self):
        # self.parentApp.options = self.options
        pass

    def afterEditing(self):
        self.parentApp.setNextForm(None)


class OptionsForm(npyscreen.ActionForm):
    def create(self):
        folder_name = self.add(npyscreen.TitleText,
                                    name = "Folder name:",
                                    value = "")
        self.options = Options(folder_name=folder_name.value)

    def on_ok(self):
        self.parentApp.options = self.options
        self.parentApp.setNextForm('TEMPLATES')


class TemplatesForm(npyscreen.ActionForm):
    def create(self):
        templates = list(self.parentApp.processor.get_templates())
        self.selected_templates = self.add(npyscreen.TitleMultiSelect,
                                   values=templates)
    def on_ok(self):
        self.parentApp.options.selected_templates = self.selected_templates.values
        self.build = True

    def on_canel(self):
        self.build = False
        

    def afterEditing(self):
        self.parentApp.setNextForm(None)
        if self.build == True:
            self.parentApp.build_dir()





class App(npyscreen.NPSAppManaged):
    def build_dir(self):
        dir_name = self.options.folder_name
        templates = self.options.selected_templates
        self.processor.build_target_dir(dir_name, *templates)

    def onStart(self):
        self.processor = Processor("rc_server.yml")
        self.options = Options()

        self.addForm("MAIN", OptionsForm, name="Options",
                     lines = 10, column = 10)
        self.addForm("TEMPLATES", TemplatesForm, name="Templates")
        # self.addForm("ALLOW", AllowForm, name="Allow", lines = 10)


if __name__ == '__main__':
    app = App()
    app.run()
