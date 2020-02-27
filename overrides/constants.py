import os
import json
from definitions import ROOT_DIR

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

SAVE_PROFILE = "SaveProfile"
SELECT_PROFILE = "SelectProfile"


list_of_method_subfolders = [file for file in os.scandir(os.path.join(ROOT_DIR, 'modules')) if file.is_dir()]
list_of_method_names = []
method_to_module_map = {}

for file in list_of_method_subfolders:
    list_of_method_names.append(file.name)
    method_to_module_map[file.name] = []
    for module in [file for file in os.scandir(os.path.join(ROOT_DIR, 'modules', file.name)) if file.is_dir()]:
        method_to_module_map[file.name].append(module.name)

list_of_profiles_subfolders = [file for file in os.scandir(os.path.join(ROOT_DIR, 'profiles')) if file.is_dir()]
list_of_profile_names = []
profiles_properties = {}

for file in list_of_profiles_subfolders:
    list_of_profile_names.append(file.name)
    with open(os.path.join(file, 'config.json')) as f:
        try:
            profiles_properties[file.name] = json.loads(f.read())
        except json.decoder.JSONDecodeError:
            continue