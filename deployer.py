import overrides.override_add_std
import npyscreen
from forms.mainform import MainForm
import overrides.shared_variables as sv

sv.init()

class App(npyscreen.NPSAppManaged):
    def onStart(self):
        self.addForm("MAIN", MainForm)


if __name__ == '__main__':
    App().run()
