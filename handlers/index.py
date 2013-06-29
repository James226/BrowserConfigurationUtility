import ConfigParser
import utils.Configuration

from Giraffe.template import *


class index(object):

    def SaveConfig(self, kw, configuration):

        for (name, value) in kw.items():
            nameParts = name.split('.')
            if len(nameParts) == 3:
                if nameParts[0] == 'configuration':
                    if not nameParts[1] in configuration.config:
                        configuration.config[nameParts[1]] = {}
                    configuration.config[nameParts[1]][nameParts[2]] = value

        completeFilename = 'config/' + kw['filename']
        if self.isValidFilename(kw['filename']) is None or not os.path.exists(completeFilename):
            return 'Invalid filename specified: ' + kw['filename']

        configuration.WriteFile(completeFilename)

    def isValidFilename(self, filename):
        return re.match("([a-zA-Z0-9\-_ \(\)]+)\.([a-zA-Z0-9\-_]+)", filename) is None

    def OutputPage(self, args, kw):
        if 'filename' not in kw:
            filename = "SampleIniFile.ini"
        else:
            filename = kw['filename']

        completeFilename = 'config/' + filename
        if self.isValidFilename(filename) or not os.path.exists(completeFilename):
            return 'Invalid filename specified: ' + filename

        configuration = utils.Configuration.Configuration()

        if 'submit' in kw:
            self.SaveConfig(kw, configuration)

        self.page = template.Load("index")
        self.page.SetVariable("ConfigFilename", filename)

        for configFilename in os.listdir('config/'):
            self.page.AddNest('fileTab', {
                'Selected': True if (configFilename == filename) else False,
                'Filename': configFilename
            })

        configuration.LoadFile(completeFilename)

        for (section, config) in configuration.config.items():
            sectionNest = self.page.AddNest("configSection", {
                'SectionName': section
            })
            for (configName, configValue) in config.items():
                self.page.AddSubNest(sectionNest, "configItem", {
                    'ConfigName': configName,
                    'ConfigValue': configValue
                })

        return self.page.OutputPage()