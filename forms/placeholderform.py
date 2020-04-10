import npyscreen
from overrides.Mixins import FormMixin


class PlaceHolderForm(FormMixin, npyscreen.ActionForm):
    def create(self):
        self.add_std(npyscreen.TitleText, name="This is a sample Form. Click OK to go back")

    def on_ok(self):
        self.parentApp.switchFormPrevious()

    def on_cancel(self):
        self.on_ok()
