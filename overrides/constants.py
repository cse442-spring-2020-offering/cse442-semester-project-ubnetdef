ADD_HOSTS = "AddHosts"
ADD_GROUP = "AddGroup"
SELECTED_HOSTS = "SelectHosts"
SELECTED_GROUP = "SelectGroup"
PLACEHOLDER_FORM = "PlaceHolderForm"
AP_NAME = "Deployer"
REMOTE_HOSTS = "Remote Hosts"
MODULES = "Modules"
MAIN_MENU_TITLE = "Menu"
SAVE_BUTTON_TEXT = "Save"
EDIT_HOSTS = "EditHosts"
EDIT_GROUP = "EditGroup"
PROFILE = 'Profiles'
modifications_made = False

import os
from definitions import ROOT_DIR
list_of_method_subfolders = [file for file in os.scandir(os.path.join(ROOT_DIR, 'modules')) if file.is_dir()]
list_of_method_names = []
method_module_map = {}

for file in list_of_method_subfolders:
    list_of_method_names.append(file.name)
    method_module_map[file.name] = []

