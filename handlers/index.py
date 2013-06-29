import ConfigParser

from Giraffe.template import *


class index(object):

    def SaveConfig(self, kw):
        configuration = {}

        for (name, value) in kw.items():
            nameParts = name.split('.')
            if len(nameParts) == 3:
                if nameParts[0] == 'configuration':
                    if not nameParts[1] in configuration:
                        configuration[nameParts[1]] = {}
                    configuration[nameParts[1]][nameParts[2]] = value

        completeFilename = 'config/' + kw['filename']
        if re.match("([a-zA-Z0-9\-_ \(\)]+)\.([a-zA-Z0-9\-_]+)", kw['filename']) is None or not os.path.exists(
                completeFilename):
            return 'Invalid filename specified: ' + kw['filename']

        config = ConfigParser.ConfigParser()
        with open(completeFilename, 'r') as fp:
            config.readfp(fp)
            for (section, configItems) in configuration.items():
                for (name, value) in configItems.items():
                    config.set(section, name, value)

        with open(completeFilename, 'w') as fp:
            config.write(fp)

    def OutputPage(self, args, kw):
        if 'filename' not in kw:
            filename = "SampleIniFile.ini"
        else:
            filename = kw['filename']

        if 'submit' in kw:
            self.SaveConfig(kw)

        self.page = template.Load("index")
        self.page.SetVariable("ConfigFilename", filename)

        completeFilename = 'config/' + filename
        if re.match("([a-zA-Z0-9\-_ \(\)]+)\.([a-zA-Z0-9\-_]+)", filename) is None or not os.path.exists(
                completeFilename):
            return 'Invalid filename specified: ' + filename

        for configFilename in os.listdir('config/'):
            self.page.AddNest('fileTab', {
                'Selected': True if (configFilename == filename) else False,
                'Filename': configFilename
            })

        config = ConfigParser.ConfigParser()
        config.readfp(open(completeFilename))
        for section in config.sections():
            sectionNest = self.page.AddNest("configSection", {
                'SectionName': section
            })
            for (configName, configValue) in config.items(section):
                self.page.AddSubNest(sectionNest, "configItem", {
                    'ConfigName': configName,
                    'ConfigValue': configValue
                })

        return self.page.OutputPage()