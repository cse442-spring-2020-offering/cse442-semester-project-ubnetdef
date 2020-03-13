import npyscreen
import overrides.shared_variables as sv
from definitions import ROOT_DIR
import os
import json
from overrides.constants import *
import cryptography

class SelectProfile(npyscreen.ActionForm):
    def create(self):
        self.select_profile_title = self.add(npyscreen.TitleText, name="Please select a profile to load", value="",
                                             editable=False, begin_entry_at=70, )
        self.group_selected = self.add(npyscreen.SelectOne, max_width=80, max_height=4, values=[
            f"{profile}{' (Encrypted)' if sv.profiles_properties[profile].get('encrypted') else ''}" for profile in
            sv.list_of_profile_names], scroll_exit=True, width=30)
        self.profile_password = self.add(npyscreen.TitlePassword,
                                         name="Password to decrypt the configuration files. (Only required for Encrypted profiles)",
                                         value="", editable=True, begin_entry_at=70, )

    @staticmethod
    def load_profile(profile_name, password=None):

        from copy import deepcopy
        old_profile = deepcopy(sv.PROFILE_CONFIG)
        old_group = deepcopy(sv.GROUPS_CONFIG)
        old_hosts = deepcopy(sv.HOSTS_CONFIG)
        try:
            target_dir = os.path.join(ROOT_DIR, 'profiles', profile_name)

            with open(os.path.join(target_dir, 'config.json')) as f:
                sv.PROFILE_CONFIG = json.loads(f.read())

            if password is not None:
                import base64
                from cryptography.hazmat.backends import default_backend
                from cryptography.hazmat.primitives import hashes
                from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC


                password = password.encode()
                salt = sv.PROFILE_CONFIG['salt'].encode('utf-8')
                kdf = PBKDF2HMAC(
                    algorithm=hashes.SHA256(),
                    length=32,
                    salt=salt,
                    iterations=100000,
                    backend=default_backend()
                )
                key = base64.urlsafe_b64encode(kdf.derive(password))
                from cryptography.fernet import Fernet
                cipher_suite = Fernet(key)

            if password is not None:
                with open(os.path.join(target_dir, 'groups.json'), 'rb') as f:
                    sv.GROUPS_CONFIG = json.loads(cipher_suite.decrypt(f.read()).decode('utf-8'))

                with open(os.path.join(target_dir, 'hosts.json'), 'rb') as f:
                    sv.HOSTS_CONFIG = json.loads(cipher_suite.decrypt(f.read()).decode('utf-8'))
            else:
                with open(os.path.join(target_dir, 'hosts.json')) as f:
                    sv.HOSTS_CONFIG = json.loads(f.read())

                with open(os.path.join(target_dir, 'groups.json')) as f:
                    sv.GROUPS_CONFIG = json.loads(f.read())
        except:
            sv.PROFILE_CONFIG = old_profile
            sv.GROUPS_CONFIG = old_group
            sv.HOSTS_CONFIG = old_hosts
            raise

    def on_ok(self):
        if self.group_selected.value:
            idx = self.group_selected.value[0]
            profile = sv.list_of_profile_names[idx]
            if sv.profiles_properties[profile].get('encrypted'):
                if self.profile_password.value:
                    try:
                        self.load_profile(profile, self.profile_password.value)
                    except cryptography.fernet.InvalidToken:
                        npyscreen.notify_confirm("Wrong Password!", wide=True, editw=1)
                        return
                    except:
                        npyscreen.notify_confirm("Something went wrong, we failed to load profile", wide=True, editw=1)
                        return

                else:
                    npyscreen.notify_confirm("Please specify password for encrypted profile", wide=True, editw=1)
                    return
            else:
                try:
                    self.load_profile(profile)
                except:
                    npyscreen.notify_confirm("Something went wrong, we failed to load profile", wide=True, editw=1)
                    return
            npyscreen.notify_confirm(f"Profile {profile} loaded successfully", wide=True, editw=1)
            sv.CHANGES_PENDING = False
            self.parentApp.getForm('MAIN').reload_screen()
            self.parentApp.switchFormPrevious()

        else:
            npyscreen.notify_confirm("Please select Profile to load", wide=True, editw=1)



    def on_cancel(self):
        self.parentApp.switchFormPrevious()
