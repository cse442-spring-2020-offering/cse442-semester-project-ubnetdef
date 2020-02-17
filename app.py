import npyscreen



def add_std(self, *args, value="", editable=False, begin_entry_at=30, **kwargs):
    self.add(npyscreen.TitleText, *args, value=value, editable=editable, begin_entry_at=begin_entry_at ,**kwargs)
npyscreen.Form.add_std = add_std

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