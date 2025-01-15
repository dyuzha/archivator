from main import Facade

import npyscreen as np

class MyApp(np.NPSAppManaged):
    def onStart(self):
        self.interface = Facade()
        self.read_rc()

    def read_rc(self):
        self.interface.read_rc_config()

    def get_opts(self):
        pass

    def archive_by_opts(self):
        self.interface.read_options_config()
        self.interface.archive_by_selected_templates()

# This form class defines the display that will be presented to the user.

class MainForm(np.Form):
    def create(self):
        self.templates = self.parentApp.tw.get_template()
        self.folder_name = self.add(np.TitleText, name = "Folder name:", value= "")
        self.selected_templates = self.add(np.TitleMultiSelect, name = "Templates:", values=self.templates)

    def afterEditing(self):
        # self.parentApp.setNextForm(None)
        self.parentApp.archive_by_opts()

if __name__ == '__main__':
    TA = MyApp()
    TA.run()
