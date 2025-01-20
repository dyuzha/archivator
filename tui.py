import npyscreen as np
from main import ArchiveTemplatesProccesor as ATP


class App(np.NPSAppManaged):
    def onStart(self):
        self.atp = ATP()

