import tomllib
import os

STORAGE_DIR = os.path.expanduser("~/.config/gentodo")
CONFIG_FILE = os.path.join(STORAGE_DIR, "config.toml")

class Config:
    def __init__(self):
        if not os.path.isfile(CONFIG_FILE):
            with open(CONFIG_FILE, "w", encoding="utf_8") as config:
                config.write("[gentodo]\n")
        self.data = self.load_config()
    
    def load_config(self):
        with open(CONFIG_FILE, "rb") as config:
            return tomllib.load(config)
    
    def get_token(self):
        try:
            return self.data['gentodo']['token']
        except KeyError:
            print("API Key not found, please add it to config.toml.")
            exit(1)

    def get_urls(self):
        try:
            return self.data['gentodo']['urls']
        except KeyError:
            print("Bugzilla URLs not found, please add them to config.toml.")
            exit(1)

    def get_emails(self):
        try:
            return self.data['gentodo']['emails']
        except KeyError:
            print("Emails not found, please add them to config.toml.")
            exit(1)
