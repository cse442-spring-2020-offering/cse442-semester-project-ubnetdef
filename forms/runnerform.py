import npyscreen
from overrides.constants import *
import overrides.shared_variables as sv
import importlib
import inspect
import threading
from importlib import reload
import traceback

class Run(npyscreen.ActionFormV2):
    SKIP_STATUS_UPDATE = False
    def run(self):

        module_name_parrent = f"modules.{sv.METHOD}.{sv.MODULE}"
        self.module_parrent = importlib.import_module(module_name_parrent)
        module_name = f"modules.{sv.METHOD}.{sv.MODULE}.main"
        self.module = importlib.import_module(module_name)

        # importlib.reload(self.module_parrent)
        # importlib.reload(self.module)


        defined_classes = [m[0] for m in inspect.getmembers(self.module, inspect.isclass) if m[1].__module__ == module_name]
        if len(defined_classes) != 1:
            npyscreen.notify_confirm("Module constructed incorrectly, one and only one class should exist in main.py",
                                     wide=True, editw=1)
            return
        try:
            class_name = defined_classes[0]
            class_to_run = getattr(self.module, class_name)
            class_instance = class_to_run()
        except Exception as e:
            npyscreen.notify_confirm(str(e), title="Module Import Error", wide=True, editw=1)
            return

        self._added_buttons['ok_button'].hidden = True
        self._added_buttons['cancel_button'].hidden = True
        self.DISPLAY()
        def thread_runner():
            try:
                class_instance.handler()
            except Exception:
                self.SKIP_STATUS_UPDATE = True
                # npyscreen.notify_confirm(str(e), title="Module Execution Error", wide=True, editw=1)
                # self.SKIP_STATUS_UPDATE = False

                self.status_field.values = str(traceback.format_exc()).split('\n')
                self.status_field.set_editable(true)

            self._added_buttons['ok_button'].hidden = False
            self._added_buttons['cancel_button'].hidden = False
            self.DISPLAY()
        th = threading.Thread(target=thread_runner)
        th.start()


    def create(self):
        self.host_selected = self.add(npyscreen.SelectOne, max_width=40, max_height=40, values=sv.SELECTIONS, scroll_exit=True, width=30)
        self.status_field = self.add(npyscreen.BufferPager, autowrap=True, values=["Select a host to get a real time update of that host!"], relx=50, rely=2,editable=False)
        self.keypress_timeout = 100

    def while_waiting(self, *args, **kwargs):
        self.update_status()
    def while_editing(self, *args, **kwargs):
        self.update_status()

    def update_status(self):
        if self.SKIP_STATUS_UPDATE:
            return
        try:
            host_to_update = self.host_selected.get_selected_objects()[0]
        except IndexError:
            return
        if host_to_update:
            with sv.lock:
                self.status_field.values = sv.UPDATE_STATUS.get(host_to_update, "No status update yet!").split('\n')
                self.DISPLAY()


    def on_ok(self):
        self.run()

    def on_cancel(self):
        self.parentApp.switchFormPrevious()
