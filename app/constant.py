import os


class Configuration:
    ROOT_DIR = os.path.abspath(os.curdir)
    CONFIGURATION_FILE = os.getenv("config_path", f"{ROOT_DIR}/.env")
