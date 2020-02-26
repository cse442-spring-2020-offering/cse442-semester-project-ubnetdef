import os
from pathlib import Path

dir_path_module_directory = os.path.dirname(os.path.realpath(__file__))
remoting_method = None
target_dir = None


def create_structure(remoting_method, module_name, force=False):

    if force:
        for root, dirs, files in os.walk(target_dir, topdown=False):
            for name in files:
                os.remove(os.path.join(root, name))
            for name in dirs:
                os.rmdir(os.path.join(root, name))
        os.rmdir(target_dir)
    os.makedirs(target_dir)
    os.makedirs(os.path.join(target_dir,"scripts"))
    with open(os.path.join(target_dir, 'config.json'), 'w') as f:
        f.write('{}')

    with open(os.path.join(target_dir, 'main.py'), 'w') as f:
        f.write(
f"""from modules.{remoting_method}.{remoting_method} import Connection{remoting_method.upper()}
class {module_name}(Connection{remoting_method.upper()}):
    def run(self):
        pass
        """)


if __name__ == '__main__':
    list_subfolders = [file for file in os.scandir(os.path.join(dir_path_module_directory, 'modules')) if
                       file.is_dir()]
    name_list_subfolders = [file.name for file in list_subfolders]
    while remoting_method not in name_list_subfolders:
        remoting_method = input(f"Enter your remoting method [{', '.join(name_list_subfolders)}]: ").strip()
    module_name = input("Module Name: ").strip()
    target_dir = os.path.join(dir_path_module_directory, 'modules', remoting_method, module_name)
    try:
        create_structure(remoting_method, module_name)
    except FileExistsError:
        force = input(f"Directory exists, would you like to OVERRIDE EVERYTHING UNDER:\n{target_dir}? [y/n]: ").strip()
        if force.lower() == 'y':
            create_structure(remoting_method, module_name, True)
        else:
            exit()

