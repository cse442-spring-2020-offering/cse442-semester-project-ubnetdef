import os
from definitions import ROOT_DIR
import threading
import json

def load_methods_and_modules():
    global list_of_method_names, method_to_module_map
    list_of_method_subfolders = [file for file in os.scandir(os.path.join(ROOT_DIR, 'modules')) if file.is_dir()]
    list_of_method_names = []
    method_to_module_map = {}
    for file in list_of_method_subfolders:
        list_of_method_names.append(file.name)
        method_to_module_map[file.name] = []
        for module in [file for file in os.scandir(os.path.join(ROOT_DIR, 'modules', file.name)) if file.is_dir()]:
            if module.name not in ['scripts', '__pycache__']:
                method_to_module_map[file.name].append(module.name)

def load_profiles():
    global list_of_profile_names, list_of_profiles_subfolders, profiles_properties
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

def init():
    global HOSTS_CONFIG, GROUPS_CONFIG, PROFILE_CONFIG, SELECTIONS, CHANGES_PENDING, list_of_method_names, method_to_module_map, list_of_method_subfolders, list_of_profiles_subfolders, list_of_profile_names, profiles_properties, MODULE, METHOD, UPDATE_STATUS, lock
    lock = threading.Lock()
    MODULE = None
    METHOD = None
    HOSTS_CONFIG = {}
    GROUPS_CONFIG = {}
    PROFILE_CONFIG = {}
    SELECTIONS = []
    UPDATE_STATUS = {}
    CHANGES_PENDING = False
    list_of_method_names = []
    method_to_module_map = {}
    list_of_method_subfolders = []
    list_of_profiles_subfolders = []
    list_of_profile_names = []
    profiles_properties = {}
    load_profiles()
    load_methods_and_modules()