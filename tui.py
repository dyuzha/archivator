from models import Processor
import npyscreen
import _curses


class TemplateList(npyscreen.MultiLineAction):
    def __init__(self, *args, **keywords):
        super(TemplateList, self).__init__(*args, **keywords)
        self.add_handlers({
            "^A": self.display_value
        })

    # @property
    # def values(self, *args, **kwargs):
    #     return self.
    def display_value(self, vl):
        return f"{vl}"

    def actionHighlighted(self, act_on_this, key_press):
        self.parent.parentApp.getForm('EDITRECORDFM').value =act_on_this[0]
        self.parent.parentApp.switchForm('EDITRECORDFM')


class TemplateListDisplay(npyscreen.FormMutt):
    MAIN_WIDGET_CLASS = TemplateList
    def beforediting(self):
        self.update_list()

    def update_list(self):
        self.wMain.value = self.parentApp.processor.get_templates()
        self.wMain.display()

class AddressBookApplication(npyscreen.NPSAppManaged):
    def onStart(self):
        self.processor = Processor("rc.yml")
        self.addForm("MAIN", TemplateListDisplay)
        # self.addForm("EDITRECORDFM", EditRecord)

if __name__ == '__main__':
    myApp = AddressBookApplication()
    myApp.run()

