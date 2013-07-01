import ConfigParser


class IniConfiguration(object):
    def LoadStream(self, stream):
        config = {}
        iniParser = ConfigParser.ConfigParser()
        iniParser.readfp(stream)
        for section in iniParser.sections():
            config[section] = {}

            for (configName, configValue) in iniParser.items(section):
                config[section][configName] = configValue

        return config

    def WriteStream(self, stream, config):
        iniParser = ConfigParser.ConfigParser()
        for (section, config) in config.items():
            iniParser.add_section(section)
            for (name, value) in config.items():
                iniParser.set(section, name, value)
        iniParser.write(stream)


from xml.etree import ElementTree

class XmlConfiguration(object):
    def LoadStream(self, stream):
        config = {}
        xmlTree = ElementTree.parse(stream)
        root = xmlTree.getroot()
        self.PopulateNode(config, root)
        return config

    def LoadChildNodes(self, currentConfigElement, xmlNode):
        for childNode in xmlNode:
            self.PopulateNode(currentConfigElement, childNode)

    def PopulateNode(self, currentConfigElement, xmlNode):
        currentConfigElement[xmlNode.tag] = {}
        self.LoadChildNodes(currentConfigElement[xmlNode.tag], xmlNode)
        if xmlNode.text is not None:
            currentConfigElement[xmlNode.tag]['Value'] = xmlNode.text

        if len(xmlNode.attrib) > 0:
            currentConfigElement[xmlNode.tag]['Attributes'] = xmlNode.attrib.copy()

    def WriteStream(self, stream, config):
        pass


class Configuration(object):
    def __init__(self):
        self.config = {}

    def LoadFile(self, filename):
        with open(filename) as fp:
            self.LoadStream(fp, "ini")

    def LoadStream(self, stream, streamType):
        if streamType == "ini":
            parser = IniConfiguration()
            self.config = parser.LoadStream(stream)

    def WriteFile(self, filename):
        with open(filename, 'w') as fp:
            self.WriteStream(fp, "ini")

    def WriteStream(self, stream, streamType):
        if streamType == "ini":
            parser = IniConfiguration()
            parser.WriteStream(stream, self.config)

