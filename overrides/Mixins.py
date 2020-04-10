import npyscreen


class FormMixin:
    def add_std(self, *args, value="", editable=False, begin_entry_at=30, **kwargs):
        return self.add(npyscreen.TitleText, *args, value=value, editable=editable, begin_entry_at=begin_entry_at ,**kwargs)
