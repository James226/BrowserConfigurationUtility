import os
import re
import time
import shutil
import utils.Configuration

from Giraffe.template import template


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

        localtime = time.localtime()
        timeString = time.strftime("%Y%m%d%H%M%S", localtime)
        fileNameParts = os.path.splitext(self.filename)
        shutil.copy(self.completeFilename, '%s%s%s' % (backupDir, timeString, fileNameParts[1]))

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

        self.configuration.LoadFile(self.completeFilename)

        self.PopulateConfigurationFromForm()

        if 'submit' in self.kwargs:
            self._SaveConfig()

        self.page = template.Load("index")
        self.page.SetVariable("ConfigFilename", self.filename)

        self.PopulateTabs()

        self.PopulateConfigurationSections()

        return self.page.OutputPage()

    def PopulateConfigurationFromForm(self):
        for (name, value) in self.kwargs.items():
            nameParts = name.split('.')
            if nameParts[0] == 'configuration':
                if len(nameParts) == 3:
                    self.PopulateExistingConfigurationFromForm(nameParts, value)
                elif len(nameParts) == 4:
                    self.PopulateNewConfigurationFromForm(nameParts, value)

    def PopulateNewConfigurationFromForm(self, splitName, value):
        if not splitName[1] in self.configuration.config:
            self.configuration.config[splitName[1]] = {}
        if not 'NewItems' in self.configuration.config[splitName[1]]:
            self.configuration.config[splitName[1]]['NewItems'] = {}
        if not splitName[3] in self.configuration.config[splitName[1]]['NewItems']:
            self.configuration.config[splitName[1]]['NewItems'][splitName[3]] = {}
        if splitName[2] == 'NewItemName':
            self.configuration.config[splitName[1]]['NewItems'][splitName[3]]['Name'] = value
        elif splitName[2] == 'NewItemValue':
            self.configuration.config[splitName[1]]['NewItems'][splitName[3]]['Value'] = value

    def PopulateExistingConfigurationFromForm(self, splitName, value):
        if not splitName[1] in self.configuration.config:
            self.configuration.config[splitName[1]] = {}
        self.configuration.config[splitName[1]][splitName[2]] = {'Value': value}

    def PopulateTabs(self):
        for configFilename in os.listdir(self.configPath):
            fileExtension = os.path.splitext(configFilename)[1]
            if fileExtension == '.ini':
                self.page.AddNest('fileTab', {
                    'Selected': True if (configFilename == self.filename) else False,
                    'Filename': configFilename
                })

    def PopulateConfigurationSections(self):
        for (section, config) in self.configuration.config.items():
            nextNewItem = 1
            sectionNest = self.page.AddNest("configSection", {
                'SectionName': section
            })
            for (configName, configValue) in config.items():
                if configName != 'Value' and configName != 'Attributes' and configName != 'NewItems':
                    self.page.AddSubNest(sectionNest, "configItem", {
                        'ConfigName': configName,
                        'ConfigValue': configValue['Value']
                    })
                elif configName == 'NewItems':
                    for (newItemName, newItemValue) in configValue.items():
                        self.page.AddSubNest(sectionNest, "newConfigItem", {
                            'ConfigNumber': str(nextNewItem),
                            'ConfigName': newItemValue['Name'],
                            'ConfigValue': newItemValue['Value']
                        })
                        nextNewItem += 1

            if 'addItem.' + section in self.kwargs:
                self.page.AddSubNest(sectionNest, "newConfigItem", {
                    'ConfigNumber': str(nextNewItem),
                    'ConfigName': '',
                    'ConfigValue': ''
                })