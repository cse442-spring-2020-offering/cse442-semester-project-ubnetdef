#!/usr/bin/env python
# encoding: utf-8

import npyscreen

def add_std(self, *args, value="", editable=False, begin_entry_at=30, **kwargs):
    self.add(npyscreen.TitleText, *args, value=value, editable=editable, begin_entry_at=begin_entry_at ,**kwargs)

npyscreen.Form.add_std = add_std

class App(npyscreen.NPSAppManaged):
    def onStart(self):
        self.addForm("MAIN", MainForm)
        self.addForm("PlaceHolderForm", PlaceHolderForm)

class PlaceHolderForm(npyscreen.ActionForm):
    def create(self):
        self.add_std(npyscreen.TitleText, name="This is a sample Form. Click OK to go back")

    def on_ok(self):
        self.parentApp.switchFormPrevious()

    def on_cancel(self):
        self.on_ok()

class MainForm(npyscreen.FormWithMenus):
    def create(self):
        self.how_exited_handers[npyscreen.wgwidget.EXITED_ESCAPE] = self.exit_application
        self.ip_selected = self.add_std(name="IP addresses Selected:")
        self.module_selected = self.add_std(name="Selected Module")
        self.module_availiable = self.add_std(name="Modules available")
        self.op_supported = self.add_std(name="Operating Systems Supported")


        self.m1 = self.add_menu(name="Menu", shortcut="H" )


        self.hosts_menu = self.m1.addNewSubmenu(name="Remote Hosts", shortcut="H", )
        self.hosts_menu.addItemsFromList([
            ("Generate New Host", self.switch_to_modules),
            ("Edit Existing Host", self.switch_to_modules),
            ("Select Host(s)", self.switch_to_modules),
            ("Create New Group", self.switch_to_modules),
            ("Edit Existing Group", self.switch_to_modules),
            ("Select Existing Group", self.switch_to_modules),
        ])

        self.modules_menu = self.m1.addNewSubmenu(name="Select Module", shortcut="M", )
        self.http = self.modules_menu.addNewSubmenu(name="HTTP", shortcut="H", )
        self.http.addItemsFromList([
            ("Module 1", self.module_placeholder),
            ("Module 2", self.module_placeholder),
            ("Module 3", self.module_placeholder),
        ])
        self.ssh = self.modules_menu.addNewSubmenu(name="SSH", shortcut="S", )
        self.ssh.addItemsFromList([
            ("Module 1", self.module_placeholder),
            ("Module 2", self.module_placeholder),
            ("Module 3", self.module_placeholder),
        ])
        self.winrm = self.modules_menu.addNewSubmenu(name="WINRM", shortcut="W", )
        self.winrm.addItemsFromList([
            ("Module 1", self.module_placeholder),
            ("Module 2", self.module_placeholder),
            ("Module 3", self.module_placeholder),
        ])
        self.modules_menu.enabled = False


        self.m1.addItemsFromList([
            ("Run", self.run_module, "R"),
            ("Help", self.display_help_msg, "^H"),
            ("Quit", self.exit_application, "Q"),
        ])

    def module_placeholder(self):
        pass

    def exit_application(self):
        self.parentApp.setNextForm(None)
        self.editing = False
        self.parentApp.switchFormNow()

    def run_module(self):
        pass

    def display_help_msg(self):
        pass

    def switch_to_modules(self):
        self.modules_menu.enabled = True
        self.parentApp.setNextForm("PlaceHolderForm")
        self.editing = False
        self.parentApp.switchFormNow()


def main():
    TA = App()
    TA.run()

if __name__ == '__main__':
    main()