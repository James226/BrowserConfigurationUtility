import os
import re
import time
import shutil
import utils.Configuration
from utils.Configuration import ConfigurationItem

from Giraffe.template import template


class index(object):
    def __init__(self, args, kw):
        self.args = args
        self.kwargs = kw
        self.configuration = utils.Configuration.Configuration()
        self.configPath = 'config/'
        self.newConfigurationItems = {}

    def SaveConfig(self):
        backupDir = self.configPath + 'backup/' + self.filename + '/'
        if not os.path.exists(backupDir):
            os.makedirs(backupDir)

        localtime = time.localtime()
        timeString = time.strftime("%Y%m%d%H%M%S", localtime)
        fileNameParts = os.path.splitext(self.filename)
        shutil.copy(self.completeFilename, '%s%s%s' % (backupDir, timeString, fileNameParts[1]))

        self.configuration.WriteFile(self.completeFilename)

    def MergeNewConfigItemsWithExisting(self):
        for (section, configSection) in self.newConfigurationItems.items():
            if self.configuration.config[section] is None:
                self.configuration.config.AddChild(ConfigurationItem(section, ''))
            for (configId, config) in configSection.items():
                self.configuration.config[section].AddChild(ConfigurationItem(config['Name'], config['Value']))
        self.newConfigurationItems = {}

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

        self.PopulateConfigurationFromForm()

        if self.configuration.config.children == []:
            self.configuration.LoadFile(self.completeFilename)

        self.ProcessEditButtons()

        if 'submit' in self.kwargs:
            self.MergeNewConfigItemsWithExisting()
            self.SaveConfig()

        self.page = template.Load("index")
        self.page.SetVariable("ConfigFilename", self.filename)

        self.PopulateTabs()

        self.PopulateConfigurationSections()

        if 'Mode' not in self.kwargs or self.kwargs['Mode'] not in ['Simple', 'Advanced']:
            if 'CurrentMode' in self.kwargs and self.kwargs['CurrentMode'] in ['Simple', 'Advanced']:
                self.kwargs['Mode'] = self.kwargs['CurrentMode']
            else:
                self.kwargs['Mode'] = 'Simple'

        self.page.SetVariable("AdvancedMode", self.kwargs['Mode'] == 'Advanced')

        return self.page.OutputPage()

    def PopulateConfigurationFromForm(self):
        for (name, value) in self.kwargs.items():
            nameParts = name.split('.')
            if nameParts[0] == 'configuration':
                if len(nameParts) == 2:
                    self.PopulateExistingSectionsFromForm(nameParts, value)
                elif len(nameParts) == 3:
                    self.PopulateExistingConfigurationFromForm(nameParts, value)
                elif len(nameParts) == 4:
                    self.PopulateNewConfigurationFromForm(nameParts, value)

    def PopulateNewConfigurationFromForm(self, splitName, value):
        if not splitName[1] in self.newConfigurationItems:
            self.newConfigurationItems[splitName[1]] = {}
        if not splitName[3] in self.newConfigurationItems[splitName[1]]:
            self.newConfigurationItems[splitName[1]][splitName[3]] = {}
        if splitName[2] == 'NewItemName':
            self.newConfigurationItems[splitName[1]][splitName[3]]['Name'] = value
        elif splitName[2] == 'NewItemValue':
            self.newConfigurationItems[splitName[1]][splitName[3]]['Value'] = value

    def PopulateExistingSectionsFromForm(self, splitName, value):
        if self.configuration.config[splitName[1]] is None:
            self.configuration.config.AddChild(ConfigurationItem(splitName[1], ''))

    def PopulateExistingConfigurationFromForm(self, splitName, value):
        if self.configuration.config[splitName[1]] is None:
            self.configuration.config.AddChild(ConfigurationItem(splitName[1], ''))
        section = self.configuration.config[splitName[1]]
        if section is None:
            section = ConfigurationItem(splitName[1], '')
            self.configuration.config.AddChild(section)

        configItem = section[splitName[2]]
        if configItem is None:
            configItem = ConfigurationItem(splitName[2], value)
            self.configuration.config[splitName[1]].AddChild(configItem)
        else:
            configItem.Value = value

    def ProcessEditButtons(self):
        for (name, value) in self.kwargs.items():
            nameParts = name.split('.')
            if nameParts[0] == 'delete':
                if len(nameParts) == 2:
                    self.configuration.config.DeleteChild(nameParts[1])
                elif len(nameParts) == 3:
                    self.configuration.config[nameParts[1]].DeleteChild(nameParts[2])

    def PopulateTabs(self):
        for configFilename in os.listdir(self.configPath):
            fileExtension = os.path.splitext(configFilename)[1]
            if fileExtension == '.ini':
                self.page.AddNest('fileTab', {
                    'Selected': True if (configFilename == self.filename) else False,
                    'Filename': configFilename
                })

    def PopulateConfigurationSections(self):
        for section in self.configuration.config:
            nextItem = 1
            nextNewItem = 1
            sectionNest = self.page.AddNest("configSection", {
                'SectionName': section.Name
            })
            for config in section:
                self.page.AddSubNest(sectionNest, "configItem", {
                    'ConfigId': str(nextItem),
                    'ConfigName': config.Name,
                    'ConfigValue': config.Value
                })
                nextItem += 1
            if section.Name in self.newConfigurationItems:
                for (newItemId, newItem) in self.newConfigurationItems[section.Name].items():
                    self.page.AddSubNest(sectionNest, "newConfigItem", {
                        'ConfigNumber': str(nextNewItem),
                        'ConfigName': newItem['Name'],
                        'ConfigValue': newItem['Value']
                    })
                    nextNewItem += 1

            if 'addItem.' + section.Name in self.kwargs:
                self.page.AddSubNest(sectionNest, "newConfigItem", {
                    'ConfigNumber': str(nextNewItem),
                    'ConfigName': '',
                    'ConfigValue': ''
                })