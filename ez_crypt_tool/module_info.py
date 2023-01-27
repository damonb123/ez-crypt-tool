"""
    Easy Crypt Tools - Module Info
    Copied from EasyPythonUtils - Allows EasyCrypt to stand alone

"""

# Python imports
import os
from os.path import exists
import re

class ModuleInfo():
    '''Parse a python .py file to get variables that start with __.
    Like the __init__.py file, or __versions__.py

    Args:
        file (str): file path to be scanned.

    Returns:
        dict: List of varibles and values found
    '''

    def __init__(self, app_file):
        self.app_path = os.path.dirname(app_file)
        self.app_vars = load_app_vars(self.app_path)
        self.app_vars['__module_path__'] = self.app_path

    def print_loaded(self):
        '''Print loaded string to console, example: Loaded [my_package/0.0.1]'''
        print( f"Loaded [{self.package_name()}/{self.version()}]" )

    def get_app_vars(self):
        '''Get dict of app variables'''
        return self.app_vars

    def module_path(self):
        '''Get module path'''
        return self.app_path

    def author(self):
        '''Get __author__'''
        return self.__get_value_safe("__author__")

    def license(self):
        '''Get __license__'''
        return self.__get_value_safe("'__license__")

    def url(self):
        '''Get __url__'''
        return self.__get_value_safe("__url__")

    def author_email(self):
        '''Get __author_email__'''
        return self.__get_value_safe("__author_email__")

    def maintainer_email(self):
        '''Get __maintainer_email__'''
        return self.__get_value_safe("__maintainer_email__")

    def package_name(self):
        '''Get __package_name__'''
        return self.__get_value_safe("__package_name__")

    def version(self):
        '''Get __version__'''
        return self.__get_value_safe("__version__")

    def __get_value_safe(self, name):
        '''
        Gets a value from a dictionary without throwing any errors.  Simple lookup.

        Args:
            dict  (dict): Source message for reference.
            name  (dict): Enrichment field results are collected in. [VALUE UPDATED]

        Returns:
            val (str): Value found during lookup.
        '''
        val = None
        try:
            val = self.app_vars[name]
        except KeyError:
            pass

        return val

def load_app_vars(app_path, p_var_dict=None):
    '''Gets __init__.py and __version__.py variables to use'''

    var_dict = {}

    # Add other dict if passed
    if p_var_dict is not None:
        var_dict.update(p_var_dict)

    var_dict = parse_app_vars( f"{app_path}/__init__.py", var_dict)
    var_dict = parse_app_vars( f"{app_path}/__version__.py", var_dict)
    return var_dict

def parse_app_vars(file, p_var_dict=None):
    '''Parses __vars__ from file passed'''
    var_dict = {}

    # Add other dict if passed
    if p_var_dict is not None:
        var_dict.update(p_var_dict)

    # pylint: disable=consider-using-with
    if exists(file):
        result = re.findall(r'(__.*__\s+=.*)', open(file, encoding="utf-8").read(), re.MULTILINE)

        # pylint: disable=invalid-name
        for s in result:
            # Split string
            name, value = s.split("=")
            # Strip and clean up variable
            name = name.strip()
            value = value.strip()
            value = value.strip(' " " ')
            value = value.strip(" ' ' ")
            # Add to dict being returned
            var_dict[name] = value

    return var_dict
