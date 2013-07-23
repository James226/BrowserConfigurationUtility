import ConfigParser
import os


class ConfigurationItem(object):
    def __init__(self, name, value, children=None):
        self.Name = name
        self.Value = value
        self.children = children if children is not None else []

    def __getitem__(self, index):
        if isinstance(index, basestring):
            for child in self.children:
                if child.Name == index:
                    return child
            return None
        else:
            return self.children[index]

    def __setitem__(self, index, value):
        if isinstance(index, basestring):
            for child in self.children:
                if child.Name == index:
                    child = value
            self.children.append(child)
        else:
            self.children[index] = value

    def AddChild(self, item):
        self.children.append(item)

    def DeleteChild(self, name):
        for child in self.children:
            if child.Name == name:
                self.children.remove(child)
        
    def __eq__(self, other):
        if isinstance(other, ConfigurationItem):
            return \
                self.Name == other.Name and \
                self.Value == other.Value and \
                all([(c == oc) for c, oc in zip(self.children, other.children)])
        return False

class IniConfiguration(object):
    def LoadStream(self, stream):
        config = ConfigurationItem('', '')
        iniParser = ConfigParser.ConfigParser()
        iniParser.readfp(stream)
        for section in iniParser.sections():
            currentSection = ConfigurationItem(section, '')
            config.AddChild(currentSection)

            for (configName, configValue) in iniParser.items(section):
                currentSection.AddChild(ConfigurationItem(configName, configValue))

        return config

    def WriteStream(self, stream, config):
        iniParser = ConfigParser.ConfigParser()
        for section in config:
            iniParser.add_section(section.Name)
            for config in section:
                iniParser.set(section.Name, config.Name, config.Value)
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
        self.config = ConfigurationItem('', '')

    def LoadFile(self, filename):
        with open(filename) as fp:
            fileExtension = os.path.splitext(filename)[1]
            self.LoadStream(fp, fileExtension)

    def LoadStream(self, stream, streamType):
        if streamType == ".ini":
            parser = IniConfiguration()
            self.config = parser.LoadStream(stream)
        elif streamType == ".xml":
            parser = XmlConfiguration()
            self.config = parser.LoadStream(stream)

    def WriteFile(self, filename):
        with open(filename, 'w') as fp:
            fileExtension = os.path.splitext(filename)[1]
            self.WriteStream(fp, fileExtension)

    def WriteStream(self, stream, streamType):
        if streamType == ".ini":
            parser = IniConfiguration()
            parser.WriteStream(stream, self.config)
        elif streamType == ".xml":
            parser = XmlConfiguration()
            parser.WriteStream(stream, self.config)

