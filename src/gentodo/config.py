'''config.py
Module that handles configuration interactions
'''

import tomllib
import sys
import os
import subprocess

CONFIG_DIR = os.path.join(
    os.environ.get("XDG_CONFIG_HOME", os.path.expanduser("~/.config")),
    "gentodo")
CONFIG_FILE = os.path.join(CONFIG_DIR, "config.toml")

class Config:
    '''Class to handle the configuration file settings'''
    def __init__(self):
        if not os.path.isfile(CONFIG_FILE):
            os.makedirs(CONFIG_DIR)
            with open(CONFIG_FILE, "w", encoding="utf_8") as config:
                config.write("[gentodo]\n")
        self.data = self.load_config()
        if "token" not in self.data:
            self.data['gentodo']['token'] = self.get_token_cmd()

    def load_config(self):
        '''Loads the config from the TOML file'''
        with open(CONFIG_FILE, "rb") as config:
            return tomllib.load(config)

    def get_token(self):
        '''Gets the Bugzilla token'''
        try:
            return self.data['gentodo']['token']
        except KeyError:
            print("API Key not found, please add it to config.toml.")
            sys.exit(1)

    def get_token_cmd(self):
        '''Gets a token from an arbitrary command'''
        try:
            token_res = subprocess.run(self.data['gentodo']['token-cmd'],
                                       stdout=subprocess.PIPE,
                                       shell=True,
                                       check=True)
            if token_res.stdout.decode() == '':
                raise ValueError("Command resulted in an empty token (invalid credentials?)")
            return token_res.stdout.decode()
        except ValueError as e:
            print(f"Error: {e}")
            sys.exit(1)
        except Exception as e:
            print("An unexpected error has occurred, please report this to the"\
                  f" Issue tracker: {e}\nhttps://github.com/csfore/gentodo/issues/new")
            sys.exit(1)

    def get_urls(self):
        '''Gets Bugzilla URLs'''
        try:
            return self.data['gentodo']['urls']
        except KeyError:
            print("Bugzilla URLs not found, please add them to config.toml.")
            sys.exit(1)

    def get_emails(self):
        '''Gets emails to search for'''
        try:
            return self.data['gentodo']['emails']
        except KeyError:
            print("Emails not found, please add them to config.toml.")
            sys.exit(1)
