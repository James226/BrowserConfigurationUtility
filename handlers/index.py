import ConfigParser
import utils.Configuration

from Giraffe.template import *


class index(object):
    def __init__(self, args, kw):
        self.args = args
        self.kwargs = kw
        self.configuration = utils.Configuration.Configuration()

    def _SaveConfig(self):

        for (name, value) in self.kwargs.items():
            nameParts = name.split('.')
            if len(nameParts) == 3:
                if nameParts[0] == 'configuration':
                    if not nameParts[1] in self.configuration.config:
                        self.configuration.config[nameParts[1]] = {}
                    self.configuration.config[nameParts[1]][nameParts[2]] = value
        self.configuration.WriteFile(self.completeFilename)

    def isValidFilename(self, filename):
        return re.match("([a-zA-Z0-9\-_ \(\)]+)\.([a-zA-Z0-9\-_]+)", filename) is None

    def OutputPage(self):

        if 'filename' not in self.kwargs:
            self.filename = "SampleIniFile.ini"
        else:
            self.filename = self.kwargs['filename']

        self.completeFilename = 'config/' + self.filename
        if self.isValidFilename(self.filename) or not os.path.exists(self.completeFilename):
            raise ValueError('Invalid filename specified: ' + self.filename)

        if 'submit' in self.kwargs:
            self._SaveConfig()

        self.page = template.Load("index")
        self.page.SetVariable("ConfigFilename", self.filename)

        for configFilename in os.listdir('config/'):
            self.page.AddNest('fileTab', {
                'Selected': True if (configFilename == self.filename) else False,
                'Filename': configFilename
            })

        self.configuration.LoadFile(self.completeFilename)

        for (section, config) in self.configuration.config.items():
            sectionNest = self.page.AddNest("configSection", {
                'SectionName': section
            })
            for (configName, configValue) in config.items():
                self.page.AddSubNest(sectionNest, "configItem", {
                    'ConfigName': configName,
                    'ConfigValue': configValue
                })

        return self.page.OutputPage()