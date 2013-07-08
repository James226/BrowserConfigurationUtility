import ConfigParser
import time
import shutil
import utils.Configuration

from Giraffe.template import *


class index(object):
    def __init__(self, args, kw):
        self.args = args
        self.kwargs = kw
        self.configuration = utils.Configuration.Configuration()
        self.configPath = 'config/'

    def _SaveConfig(self):
        backupDir = self.configPath + 'backup/' + self.filename + '/'
        if not os.path.exists(backupDir):
            os.makedirs(backupDir)

        localtime   = time.localtime()
        timeString  = time.strftime("%Y%m%d%H%M%S", localtime)
        fileNameParts = os.path.splitext(self.filename)
        shutil.copy(self.completeFilename, '%s%s%s' % (backupDir, timeString, fileNameParts[1]))
        
        for (name, value) in self.kwargs.items():
            nameParts = name.split('.')
            if len(nameParts) == 3:
                if nameParts[0] == 'configuration':
                    if not nameParts[1] in self.configuration.config:
                        self.configuration.config[nameParts[1]] = {}
                    self.configuration.config[nameParts[1]][nameParts[2]] = {'Value': value}
        self.configuration.WriteFile(self.completeFilename)

    def isValidFilename(self, filename):
        return re.match("([a-zA-Z0-9\-_ \(\)]+)\.([a-zA-Z0-9\-_]+)", filename) is None

    def OutputPage(self):

        if 'filename' not in self.kwargs:
            self.filename = "SampleIniFile.ini"
        else:
            self.filename = self.kwargs['filename']

        self.completeFilename = self.configPath + self.filename
        if self.isValidFilename(self.filename) or not os.path.exists(self.completeFilename):
            return 'Invalid filename specified: ' + self.filename

        if 'submit' in self.kwargs:
            self._SaveConfig()

        self.page = template.Load("index")
        self.page.SetVariable("ConfigFilename", self.filename)

        for configFilename in os.listdir(self.configPath):
            fileExtension = os.path.splitext(configFilename)[1]
            if fileExtension == '.ini':
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
                if configName != 'Value' and configName != 'Attributes':
                    self.page.AddSubNest(sectionNest, "configItem", {
                        'ConfigName': configName,
                        'ConfigValue': configValue['Value']
                    })

        return self.page.OutputPage()
