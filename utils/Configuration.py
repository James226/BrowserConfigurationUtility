import ConfigParser


class Configuration(object):
    def __init__(self):
        self.config = {}

    def LoadFile(self, filename):
        with open(filename) as fp:
            self.LoadStream(fp)

    def LoadStream(self, stream):
        iniParser = ConfigParser.ConfigParser()
        iniParser.readfp(stream)
        for section in iniParser.sections():
            self.config[section] = {}

            for (configName, configValue) in iniParser.items(section):
                self.config[section][configName] = configValue

    def WriteFile(self, filename):
        with open(filename, 'w') as fp:
            self.WriteStream(fp)

    def WriteStream(self, stream):
        iniParser = ConfigParser.ConfigParser()
        for (section, config) in self.config.items():
            iniParser.add_section(section)
            for (name, value) in config.items():
                iniParser.set(section, name, value)
        iniParser.write(stream)
