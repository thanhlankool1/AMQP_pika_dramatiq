from __future__ import absolute_import, unicode_literals
import configparser
import os


class Config(object):
    FILE_NAME = 'config_dev.ini'
    APP_DIR = os.getcwd()
    CONFIG_FILE = os.path.join(os.path.join(APP_DIR, 'etc'), FILE_NAME)

    def __init__(self):
        self.config = configparser.ConfigParser()

        if self.config is not None:
            self.config.read(self.CONFIG_FILE)

    def _get(self, section, option, default=None):
        """
        Will check if section.option exists in config_file, return its value, default
        otherwise
        """

        if not self.config.has_section(section):
            return default
        if not self.config.has_option(section, option):
            return default
        if self.config.get(section, option) == 'None':
            return None

        return self.config.get(section, option)


global_config = Config()
