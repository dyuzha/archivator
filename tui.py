from models import Processor
import npyscreen
from dataclasses import dataclass

@dataclass
class Options:
    folder_name: str = "Bases"


class TemplateList(npyscreen.MultiSelectAction):
    def __init__(self, *args, **keywords):
        super(TemplateList, self).__init__(*args, **keywords)
        self.add_handlers({
            # "r": self.h_find_char(input),
            "e": self.exit()
         })

    def update_options(self):
        self.parent.parentApp.setNextForm("OPTIONS")

    def display_value(self, vl):
        return f"{vl}"

    def exit(self):
        pass
        
    def actionHighlighted(self, act_on_this, key_press):
        "Override this Method"
        pass
    
    def actionSelected(self, act_on_these, keypress):
        "Override this Method"
        pass
    

class OptionsForm(npyscreen.ActionForm):
    def create(self):
        folder_name = self.add(npyscreen.TitleText,
                                    name = "Folder name: ",
                                    value = "")

        self.options = Options(folder_name=folder_name.value)

    def on_ok(self):
        self.parentApp.options = self.options
        self.parentApp.setNextForm("MAIN")


class TemplateListDisplay(npyscreen.FormMutt):
    MAIN_WIDGET_CLASS = TemplateList
    def beforeEditing(self):
        self.update_list()

    def update_list(self):
        self.wMain.values = list(self.parentApp.processor.get_templates())
        self.wMain.display()


class App(npyscreen.NPSAppManaged):
    @property
    def options(self):
        return self._options

    @options.setter
    def options(self, value):
        self._options = value

    def onStart(self):
        self.processor = Processor("rc.yml")
        self.addForm("MAIN", TemplateListDisplay, name="Templates")
        self.addForm("OPTIONS", OptionsForm, name="Options")


if __name__ == '__main__':
    app = App()
    app.run()
