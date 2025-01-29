from models import Processor
import npyscreen
from dataclasses import dataclass, field


@dataclass
class Options:
    folder_name: str = "Bases"
    selected_templates: list = field(default_factory=list)


class OptionsForm(npyscreen.ActionForm):
    def create(self):
        self.folder_name = self.add(npyscreen.TitleText,
                                    name = "Folder name:",
                                    value = "")
        

    def on_ok(self):
        self.parentApp.options.folder_name = self.folder_name.value
        self.parentApp.setNextForm('TEMPLATES')


class TemplatesForm(npyscreen.ActionForm):
    def create(self):
        templates = list(self.parentApp.processor.get_templates())
        self.templates = self.add(npyscreen.TitleMultiSelect,
                                   values=templates)
    def on_ok(self):
        self.parentApp.options.selected_templates = self.templates.get_selected_objects()
        self.parentApp.build = True

    def on_canel(self):
        self.parentApp.build = False
        

    def afterEditing(self):
        self.parentApp.switchForm(None)


class App(npyscreen.NPSAppManaged):
    build: bool

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
