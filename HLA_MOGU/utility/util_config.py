# -*- coding: utf-8 -*-
import os
from configparser import ConfigParser

CONFIG_FILENAME = 'config.ini'


def get_config():
    config = ConfigParser()
    current_py = os.path.abspath(__file__)
    current_directory = os.path.dirname(current_py)
    root_directory = os.path.dirname(current_directory)
    config_file = os.path.join(root_directory, CONFIG_FILENAME)
    config.read(config_file)
    return config


def get_config_value(section, option):
    config = get_config()
    value = config.get(section, option)
    return value


def test():
    value = get_config_value('log_conf', 'log_path')
    print(value)


if __name__ == '__main__':
    test()
