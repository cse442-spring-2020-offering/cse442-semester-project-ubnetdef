import npyscreen
import overrides.shared_variables as sv
from overrides.constants import *
class SaveProfile(npyscreen.ActionForm):
    def create(self):
        self.OK_BUTTON_TEXT = SAVE_BUTTON_TEXT
        self.profile_name = self.add(npyscreen.TitleText, name="Provide a Name for your profile: ", value="", editable=True, begin_entry_at=70, )
        self.encrypt = self.add(npyscreen.Checkbox, name="Encrypt the profile?")
        self.encrypt.whenToggled = self.unhide_pass
        self.profile_password = self.add(npyscreen.TitlePassword, name="Password to encrypt the configuration files", value="", editable=True, begin_entry_at=70, )
        self.profile_password.hidden = True

    @staticmethod
    def create_profile(profile_name, password=None, force=False):
        import json

        target_dir = os.path.join(ROOT_DIR, 'profiles', profile_name)
        if force and os.path.isdir(target_dir):
            for root, dirs, files in os.walk(target_dir, topdown=False):
                for name in files:
                    os.remove(os.path.join(root, name))
                for name in dirs:
                    os.rmdir(os.path.join(root, name))
            os.rmdir(target_dir)

        os.makedirs(target_dir)

        if password is not None:
            sv.PROFILE_CONFIG['encrypted'] = True
            import base64
            from cryptography.hazmat.backends import default_backend
            from cryptography.hazmat.primitives import hashes
            from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
            password = password.encode()
            salt = b'salt_'  # Acts as pepper
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

        with open(os.path.join(target_dir, 'config.json'), 'w') as f:
            f.write(json.dumps(sv.PROFILE_CONFIG))


        if password is not None:
            with open(os.path.join(target_dir, 'groups.json'), 'wb') as f:
                encoded_text = cipher_suite.encrypt(json.dumps(sv.GROUPS_CONFIG).encode('utf-8'))
                f.write(encoded_text)

            with open(os.path.join(target_dir, 'hosts.json'), 'wb') as f:
                encoded_text = cipher_suite.encrypt(json.dumps(sv.HOSTS_CONFIG).encode('utf-8'))
                f.write(encoded_text)

        else:
            with open(os.path.join(target_dir, 'groups.json'), 'w') as f:
                f.write(json.dumps(sv.GROUPS_CONFIG))
            with open(os.path.join(target_dir, 'hosts.json'), 'w') as f:
                f.write(json.dumps(sv.HOSTS_CONFIG))

    def unhide_pass(self):
        self.profile_password.hidden = not self.profile_password.hidden
        self.DISPLAY()


    def on_ok(self):
        if self.profile_name.value:
            if self.profile_name.value in list_of_profile_names and not npyscreen.notify_yes_no(
                        f"Profile {self.profile_name.value} already exists, would you like to override?",
                        title="Already Exists", editw=1):
                return

            if self.profile_password.hidden:
                self.create_profile(self.profile_name.value, force=True)

            elif not self.profile_password.value:
                npyscreen.notify_confirm("Please provide password", wide=True, editw=1)
                return
            else:
                self.create_profile(self.profile_name.value, password=self.profile_password.value, force=True)
                npyscreen.notify_confirm("Profile Saved successfully!", wide=True, editw=1)
            sv.CHANGES_PENDING = False
            self.parentApp.switchFormPrevious()
        else:
            npyscreen.notify_confirm("Please specify profile name", wide=True, editw=1)

    def on_cancel(self):
        self.parentApp.switchFormPrevious()