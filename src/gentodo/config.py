'''config.py
Module that handles configuration interactions
'''

import tomllib
import sys
import os

STORAGE_DIR = os.path.expanduser("~/.config/gentodo")
CONFIG_FILE = os.path.join(STORAGE_DIR, "config.toml")

class Config:
    '''Class to handle the configuration file settings'''
    def __init__(self):
        if not os.path.isfile(CONFIG_FILE):
            os.makedirs(STORAGE_DIR)
            with open(CONFIG_FILE, "w", encoding="utf_8") as config:
                config.write("[gentodo]\n")
        self.data = self.load_config()

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
