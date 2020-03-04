import npyscreen
import art
from npyscreen import utilNotify
import overrides.shared_variables as sv
import overrides.constants
from overrides.constants import *
from forms.selectmodule import SelectModule
from forms.hosts_forms.addhosts import AddHosts
from forms.placeholderform import PlaceHolderForm
from forms.hosts_forms.addgroup import AddGroup
from forms.hosts_forms.selecthosts import SelectHosts
from forms.hosts_forms.selectgroup import SelectGroup
from forms.saveprofile import SaveProfile
from forms.selectprofile import SelectProfile


class MainForm(npyscreen.FormWithMenus):
    def create(self):
        self.how_exited_handers[npyscreen.wgwidget.EXITED_ESCAPE] = self.exit_application
        self.ip_availiable = self.add_std(name="Hosts Available:")
        self.groups_availiable = self.add_std(name="Groups Available:")
        self.ip_selected = self.add_std(name="Host(s) Selected:")
        self.module_selected = self.add_std(name="Selected Module")
        self.module_availiable = self.add_std(name="Modules available")
        self.os_supported = self.add_std(name="Operating Systems Supported")

        self.m1 = self.add_menu(name=MAIN_MENU_TITLE)
        self.hosts_menu = self.m1.addNewSubmenu(name=REMOTE_HOSTS, shortcut="^H")
        self.hosts_menu.addItemsFromList([
            ("Add Or Edit Host", self.switch_to_form, None, None, (ADD_HOSTS, AddHosts,)),
            ("Select Host(s)", self.select_host),
            ("Add Or Edit Group", self.add_group),
            ("Select Existing Group", self.select_group),
        ])
        self.m1.addItemsFromList([
            ("Modules", self.module_selector),
            ("Run", self.run_module),
            ("Select Profile", self.select_profile),
            ("Save Profile", self.switch_to_form, None, None, (SAVE_PROFILE, SaveProfile,)),
            ("Quit", self.exit_application, "^Q"),
            ("Help", self.display_help_msg),
        ])
        self.reload_screen()

    def form_exists_in_application(self, id):
        return id in self.parentApp._Forms

    def no_hosts_created_alert(self):
        npyscreen.notify_confirm(f"No Hosts were created. Please add Hosts to continue",
                                 title="Information Missing/Incorrect", wide=True, editw=1)
    def add_group(self):
        if len(sv.HOSTS_CONFIG.keys()) != 0:
            self.switch_to_form(ADD_GROUP, AddGroup)
        else:
            self.no_hosts_created_alert()


    def select_host(self):
        if len(sv.HOSTS_CONFIG.keys()) != 0:
            self.switch_to_form(SELECTED_HOSTS, SelectHosts)
        else:
            self.no_hosts_created_alert()

    def select_group(self):
        if len(sv.HOSTS_CONFIG.keys()) != 0 and len(sv.GROUPS_CONFIG.keys()) != 0:
            self.switch_to_form(SELECTED_GROUP, SelectGroup)
        else:
            npyscreen.notify_confirm(f"No Hosts or Groups were created. Please add Host(s) and Group(s) to continue",
                                 title="Information Missing/Incorrect", wide=True, editw=1)

    def select_profile(self):
        response = True
        if sv.CHANGES_PENDING:
            response = npyscreen.notify_ok_cancel(
                "You have unsaved changes in hosts configuration, or groups configuration",
                title="Information Missing/Incorrect\nWould you like to switch profiles before saving current profile?",
                editw=0)
        if response:
            self.switch_to_form(SELECT_PROFILE, SelectProfile)

    def module_selector(self):
        if sv.SELECTIONS:
            for host in sv.SELECTIONS:
                if sv.HOSTS_CONFIG[host]['method'] != sv.HOSTS_CONFIG[sv.SELECTIONS[0]]['method']:
                    npyscreen.notify_confirm("Hosts do not share common remoting method", wide=True, editw=1)
                    return
            self.switch_to_form(MODULES, SelectModule)
        else:
            npyscreen.notify_confirm(
                "No Hosts/Group were selected. Please go to Hosts Menu, to select hosts or a group",
                title="No Hosts/Group Selected", wide=True, editw=1)

    def exit_application(self):
        self.parentApp.setNextForm(None)
        self.editing = False
        self.parentApp.switchFormNow()

    def reload_screen(self):
        self.ip_availiable.set_value(", ".join(sv.HOSTS_CONFIG.keys()))
        self.ip_selected.set_value(", ".join(sv.SELECTIONS))
        self.groups_availiable.set_value(", ".join(sv.GROUPS_CONFIG))
        self.DISPLAY()

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
        PopupWide.DEFAULT_LINES = int(len(help_msg.splitlines()) * 1.2)
        npyscreen.notify_confirm(help_msg, title="Help", wide=True, editw=1)

    def switch_to_form(self, argument=PLACEHOLDER_FORM, form_id=PlaceHolderForm):
        if self.form_exists_in_application(argument):
            self.parentApp.removeForm(argument)
        self.parentApp.addForm(argument, form_id)
        self.parentApp.setNextForm(argument)
        self.editing = False
        self.parentApp.switchFormNow()
