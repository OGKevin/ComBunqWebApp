import configparser

import os


class ConfigController:
    """A controller class for getting and setting key/value pairs 
    in the config file
    """

    section_default = 'BunqAPI'

    def __init__(self):
        """Create an instance of a config controller for getting 
        and setting information
        """

        self.path = os.path.dirname(os.path.realpath(__file__)) \
                    + '/parameters.ini'
        self.parser = configparser.ConfigParser()
        self.parser.read(self.path)

    def get(self, name, section=section_default):
        """Returns a value with a given name from the configuration file."""
        try:
            return self.parser[section][name]
        except KeyError:
            return None

    def set(self, name, val, section=section_default):
        """Sets an entry in the default section of the config file to a 
        specified value
        :param section: [Optional] The section in which an entry 
        should be changed
        :param name: The entry whose value should be changed
        :param val: The new value for the specified entry
        :return: Nothing, but happiness
        """
        if section not in self.parser.sections():
            self.parser.add_section(section)

        self.parser.set(section, name, val)
        self.save()

    def save(self):
        """Saves the changes to the config file.
        """
        file = open(self.path, 'w')
        self.parser.write(file)
        file.close()
