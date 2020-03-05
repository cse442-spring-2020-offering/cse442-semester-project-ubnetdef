import npyscreen
from overrides.constants import *
import overrides.shared_variables as sv
import importlib
import inspect

class Run(npyscreen.SplitForm):
    def run(self):
        module_name = f"modules.{sv.METHOD}.{sv.MODULE}.main"
        module = importlib.import_module(module_name)
        defined_classes = [m[0] for m in inspect.getmembers(module, inspect.isclass) if m[1].__module__ == module_name]
        if len(defined_classes) != 1:
            npyscreen.notify_confirm("Module constructed incorrectly, only one class should exist in main.py",
                                     wide=True, editw=1)
            return

        class_name = defined_classes[0]
        class_to_run = getattr(module, class_name)
        class_instance = class_to_run()
        # class_instance.run()

    def create(self):
        self.run_button = self.add(npyscreen.ButtonPress, name="Run")
        self.run_button.whenPressed = self.run


    def on_ok(self):
        self.parentApp.switchForm('MAIN')


    def on_cancel(self):
        self.parentApp.switchForm('MAIN')
