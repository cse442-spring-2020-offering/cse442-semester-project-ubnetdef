import npyscreen
def add_std(self, *args, value="", editable=False, begin_entry_at=30, **kwargs):
    self.add(npyscreen.TitleText, *args, value=value, editable=editable, begin_entry_at=begin_entry_at ,**kwargs)
npyscreen.Form.add_std = add_std