import configparser

import os


class Controller:
    """A controller class for getting and setting key/value pairs 
    in the config file
    """

    __section_default = 'BunqAPI'
    __dir_path = os.path.dirname(os.path.abspath(__file__))
    __default_filepath = '%s/parameters.ini' % __dir_path

    def __init__(self, filepath=None):
        """Create an instance of a config controller for getting 
        and setting information
        """
        self.path = self.__default_filepath if filepath is None else filepath
        self.parser = configparser.ConfigParser()
        if self.__section_default not in self.parser.sections():
            self.parser.add_section(self.__section_default)

        self.parser.read(self.path)

    def get(self, name, section=__section_default):
        """Returns a value with a given name from the configuration file."""
        
        if self.parser.has_option(section, name):
            return self.parser[section][name]
        else:
            return None

    def set(self, name, val, section=__section_default):
        """Sets an entry in the default section of the config file to a 
        specified value

        If the entry should be set to None, this function will delete it
        from the config file.

        :param section: [Optional] The section in which an entry 
        should be changed
        :param name: The entry whose value should be changed
        :param val: The new value for the specified entry
        :return: Nothing, but happiness
        """
        if section not in self.parser.sections():
            self.parser.add_section(section)

        if val is None:
            if self.parser.has_option(section, name):
                self.parser.remove_option(section, name)
        else:
            self.parser.set(section, name, str(val))
            
        self.save()

    def save(self):
        """Saves the changes to the config file.
        """
        file = open(self.path, 'w')
        self.parser.write(file)
        file.close()
