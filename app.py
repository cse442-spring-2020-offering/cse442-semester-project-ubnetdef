import npyscreen
import overrides.override_add_std

from forms.main_form import main_form
from forms.place_holder_form import place_holder_form

class App(npyscreen.NPSAppManaged):
    def onStart(self):
        self.addForm("MAIN", main_form)
        self.addForm("PlaceHolderForm", place_holder_form)

def main():
    TA = App()
    TA.run()

if __name__ == '__main__':
    main()