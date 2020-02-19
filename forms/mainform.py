import npyscreen
import art
from npyscreen import utilNotify
from overrides.constants import *


class MainForm(npyscreen.FormWithMenus):
    def create(self):
        self.how_exited_handers[npyscreen.wgwidget.EXITED_ESCAPE] = self.exit_application
        self.ip_selected = self.add_std(name="IP addresses Selected:")
        self.module_selected = self.add_std(name="Selected Module")
        self.module_availiable = self.add_std(name="Modules available")
        self.op_supported = self.add_std(name="Operating Systems Supported")

        self.m1 = self.add_menu(name=MAIN_MENU_TITLE)

        self.hosts_menu = self.m1.addNewSubmenu(name=REMOTE_HOSTS, shortcut="^H")
        self.hosts_menu.addItemsFromList([
            ("Add New Host", self.switch_to_form, None, None, (ADD_HOSTS,)),
            ("Edit Existing Host", self.switch_to_form),
            ("Select Host(s)", self.switch_to_form, None, None, (SELECTED_HOSTS,)),
            ("Add New Group", self.switch_to_form, None, None, (ADD_GROUP,)),
            ("Edit Existing Group", self.switch_to_form),
            ("Select Existing Group", self.switch_to_form, None, None, (SELECTED_GROUP,)),
        ])

        self.modules_menu = self.m1.addNewSubmenu(name=MODULES, shortcut="^M", )
        self.http = self.modules_menu.addNewSubmenu(name="HTTP", shortcut="^H", )
        self.http.addItemsFromList([
            ("Module 1", self.module_selector, None, None, ("HTTP","Module 1",)),
            ("Module 2", self.module_selector, None, None, ("HTTP","Module 2",)),
            ("Module 3", self.module_selector, None, None, ("HTTP","Module 3",)),
        ])
        self.ssh = self.modules_menu.addNewSubmenu(name="SSH", shortcut="^S", )
        self.ssh.addItemsFromList([
            ("Module 1", self.module_selector, None, None, ("SSH","Module 1",)),
            ("Module 2", self.module_selector, None, None, ("SSH","Module 2",)),
            ("Module 3", self.module_selector, None, None, ("SSH","Module 3",)),
        ])
        self.winrm = self.modules_menu.addNewSubmenu(name="WINRM", shortcut="^W", )
        self.winrm.addItemsFromList([
            ("Module 1", self.module_selector, None, None, ("WINRM","Module 1",)),
            ("Module 2", self.module_selector, None, None, ("WINRM","Module 2",)),
            ("Module 3", self.module_selector, None, None, ("WINRM","Module 3",)),
        ])
        self.modules_menu.enabled = False


        self.m1.addItemsFromList([
            ("Run", self.run_module, "^R"),
            ("Quit", self.exit_application, "^Q"),
            ("Help", self.display_help_msg),
        ])

    def module_selector(self, method, module):
        self.module_selected.set_value(f"{method}/{module}")

    def module_placeholder(self):
        pass

    def exit_application(self):
        self.parentApp.setNextForm(None)
        self.editing = False
        self.parentApp.switchFormNow()

    def run_module(self):
        pass


    def display_help_msg(self):

        help_msg = f"""{art.text2art("UBNetDef", "random")}
Welcome to {AP_NAME}!
Deployer is a multi stage application that allows the user to deploy a preset modules on remote hosts using availiable methods like SSH(Linux), HTTP(WebApps), and WINRM(Windows).
To start using Deployer follow the steps below:
1. Select the Host(s) from {REMOTE_HOSTS} menu. If no Hosts are defined, generate a new Host under {REMOTE_HOSTS} menu.
2. Once the Host(s) selected, navigate back to menu and select the desired Module from {MODULES} menu.
3. Evaluate the selected Module and selected Hosts(s) on the main screen.
4. Use Run button to run the desired module on a selected host.
"""
        from npyscreen.fmPopup import PopupWide
        PopupWide.DEFAULT_LINES = int(len(help_msg.splitlines())*1.2)
        npyscreen.notify_confirm(help_msg, title="Help", wide=True, editw=1)

    def switch_to_form(self, argument=PLACEHOLDER_FORM):
        self.modules_menu.enabled = True
        self.parentApp.setNextForm(argument)
        self.editing = False
        self.parentApp.switchFormNow()


