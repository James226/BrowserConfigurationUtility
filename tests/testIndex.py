import os
import unittest

import handlers.index


class TestIndex(unittest.TestCase):
    def test_hasDefaultConfigFilename(self):
        indexPage = handlers.index.index((), {})
        indexPage.OutputPage()

        self.assertEqual(indexPage.filename, 'SampleIniFile.ini')
        self.assertEqual(indexPage.page.page.Nests['']['ConfigFilename'], 'SampleIniFile.ini')

    def test_shouldSaveConfigurationWhenSubmitButtonPressed(self):
        indexPage = handlers.index.index((), {'submit': 'Save'})
        global configurationSaved
        configurationSaved = False

        def saveConfiguration():
            global configurationSaved
            configurationSaved = True

        indexPage._SaveConfig = saveConfiguration
        indexPage.OutputPage()

        self.assertTrue(configurationSaved)

    def test_shouldPopulatePageWithConfigurationItems(self):
        indexPage = handlers.index.index((), {})
        indexPage.configuration.LoadFile = lambda filename: 0
        indexPage.configuration.config = {
            'Section1': {
                'Variable1': {'Value': 'TestA'},
                'Variable2': {'Value': 'TestB'}
            }, 'Section2': {
                'Variable3': {'Value': 'TestC'}
            }}

        indexPage.OutputPage()

        self.assertDictContainsSubset({'SectionName': 'Section2'},
                                      indexPage.page.page.Nests['configSection'][0])

        self.assertDictContainsSubset({'SectionName': 'Section1'},
                                      indexPage.page.page.Nests['configSection'][1])

        self.assertDictEqual({'ConfigName': 'Variable3', 'ConfigValue': 'TestC'},
                             indexPage.page.page.Nests['configSection'][0]['configItem'][0])

        self.assertDictEqual({'ConfigName': 'Variable2', 'ConfigValue': 'TestB'},
                             indexPage.page.page.Nests['configSection'][1]['configItem'][1])

    def test_shouldFilterDisplayedFilesBasedOnFileType(self):
        indexPage = handlers.index.index((), {})

        os.listdir = lambda path: ['Config1.ini', 'DirName', 'Config2.dat', 'Config3.config', 'Config4.ini']
        indexPage.configuration.LoadFile = lambda filename: 0

        indexPage.OutputPage()

        self.assertEqual(indexPage.page.page.Nests['fileTab'][0]['Filename'], 'Config1.ini')
        self.assertEqual(indexPage.page.page.Nests['fileTab'][1]['Filename'], 'Config4.ini')

    def test_ShouldAddNewConfigItemWhenAddItemButtonPressed(self):
        indexPage = handlers.index.index((), {'addItem.Section1': '+'})

        indexPage.configuration.LoadFile = lambda filename: 0
        indexPage.configuration.config = {
            'Section1': {
                'Variable1': {'Value': 'TestA'},
                'Variable2': {'Value': 'TestB'}
            }, 'Section2': {
                'Variable3': {'Value': 'TestC'}
            }}

        indexPage.OutputPage()

        self.assertListEqual([{'ConfigNumber': '1', 'ConfigName': '', 'ConfigValue': ''}],
                             indexPage.page.page.Nests['configSection'][1]['newConfigItem'])

    def test_ShouldRememberExistingConfigurationWhenNonSaveButtonPressed(self):
        indexPage = handlers.index.index((), {
            'configuration.Section1.Variable1': 'TestD',
            'configuration.Section1.Variable2': 'TestE',
            'configuration.Section2.Variable1': 'TestF'
        })

        indexPage.configuration.LoadFile = lambda filename: 0
        indexPage.configuration.config = {
            'Section1': {
                'Variable1': {'Value': 'TestA'},
                'Variable2': {'Value': 'TestB'}
            }, 'Section2': {
                'Variable1': {'Value': 'TestC'}
            }}

        indexPage.OutputPage()

        self.assertDictEqual({'ConfigName': 'Variable1', 'ConfigValue': 'TestF'},
                             indexPage.page.page.Nests['configSection'][0]['configItem'][0])

        self.assertDictEqual({'ConfigName': 'Variable2', 'ConfigValue': 'TestE'},
                             indexPage.page.page.Nests['configSection'][1]['configItem'][1])

    def test_ShouldNotRememberNewItemNameOrValueAsExistingItems(self):
        indexPage = handlers.index.index((), {
            'configuration.Section1.Variable1': 'TestD',
            'configuration.Section1.Variable2': 'TestE',
            'configuration.Section2.Variable1': 'TestF',
            'configuration.Section2.NewItemName.1': 'Variable2',
            'configuration.Section2.NewItemValue.1': 'TestG'
        })

        indexPage.configuration.LoadFile = lambda filename: 0
        indexPage.configuration.config = {
            'Section1': {
                'Variable1': {'Value': 'TestA'},
                'Variable2': {'Value': 'TestB'}
            }, 'Section2': {
                'Variable1': {'Value': 'TestC'}
            }}

        indexPage.OutputPage()

        for configItem in indexPage.page.page.Nests['configSection'][0]['configItem']:
            self.assertNotEqual('NewItemName.1', configItem['ConfigName'])
            self.assertNotEqual('NewItemValue.1', configItem['ConfigName'])

    def test_ShouldRememberNewItems(self):
        indexPage = handlers.index.index((), {
            'configuration.Section1.Variable1': 'TestD',
            'configuration.Section1.Variable2': 'TestE',
            'configuration.Section2.Variable1': 'TestF',
            'configuration.Section2.NewItemName.1': 'Variable2',
            'configuration.Section2.NewItemValue.1': 'TestG'
        })

        indexPage.configuration.LoadFile = lambda filename: 0
        indexPage.configuration.config = {
            'Section1': {
                'Variable1': {'Value': 'TestA'},
                'Variable2': {'Value': 'TestB'}
            }, 'Section2': {
                'Variable1': {'Value': 'TestC'}
            }}

        indexPage.OutputPage()

        self.assertListEqual(
            [
                {'ConfigNumber': '1', 'ConfigName': 'Variable2', 'ConfigValue': 'TestG'}
            ],
            indexPage.page.page.Nests['configSection'][0]['newConfigItem'])