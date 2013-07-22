import os
import unittest

import handlers.index
from utils.Configuration import ConfigurationItem


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

        indexPage.SaveConfig = saveConfiguration
        indexPage.OutputPage()

        self.assertTrue(configurationSaved)

    def test_shouldPopulatePageWithConfigurationItems(self):
        indexPage = handlers.index.index((), {})
        indexPage.configuration.LoadFile = lambda filename: 0
        indexPage.configuration.config = \
            ConfigurationItem('', '', [
                ConfigurationItem('Section1', '', [
                    ConfigurationItem('Variable1', 'TestA'),
                    ConfigurationItem('Variable2', 'TestB')
                ]),
                ConfigurationItem('Section2', '', [
                    ConfigurationItem('Variable3', 'TestC')
                ])
            ])

        indexPage.OutputPage()

        self.assertDictContainsSubset({'SectionName': 'Section1'},
                                      indexPage.page.page.Nests['configSection'][0])

        self.assertDictContainsSubset({'SectionName': 'Section2'},
                                      indexPage.page.page.Nests['configSection'][1])

        self.assertDictEqual({'ConfigId': '2', 'ConfigName': 'Variable2', 'ConfigValue': 'TestB'},
                             indexPage.page.page.Nests['configSection'][0]['configItem'][1])

        self.assertDictEqual({'ConfigId': '1', 'ConfigName': 'Variable3', 'ConfigValue': 'TestC'},
                             indexPage.page.page.Nests['configSection'][1]['configItem'][0])

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
        indexPage.configuration.config = \
            ConfigurationItem('', '', [
                ConfigurationItem('Section1', '', [
                    ConfigurationItem('variable1', 'TestA'),
                    ConfigurationItem('variable2', 'TestB')
                ]),
                ConfigurationItem('Section2', '', [
                    ConfigurationItem('variable3', 'TestC')
                ])
            ])

        indexPage.OutputPage()

        self.assertListEqual([{'ConfigNumber': '1', 'ConfigName': '', 'ConfigValue': ''}],
                             indexPage.page.page.Nests['configSection'][0]['newConfigItem'])

    def test_ShouldRememberExistingConfigurationWhenNonSaveButtonPressed(self):
        indexPage = handlers.index.index((), {
            'configuration.Section1.Variable1': 'TestD',
            'configuration.Section1.Variable2': 'TestE',
            'configuration.Section2.Variable1': 'TestF'
        })

        indexPage.configuration.LoadFile = lambda filename: 0
        indexPage.configuration.config = \
            ConfigurationItem('', '', [
                ConfigurationItem('Section1', '', [
                    ConfigurationItem('Variable1', 'TestA'),
                    ConfigurationItem('Variable2', 'TestB')
                ]),
                ConfigurationItem('Section2', '', [
                    ConfigurationItem('Variable1', 'TestC')
                ])
            ])

        indexPage.OutputPage()

        self.assertDictEqual({'ConfigId': '1', 'ConfigName': 'Variable1', 'ConfigValue': 'TestF'},
                             indexPage.page.page.Nests['configSection'][1]['configItem'][0])

        self.assertDictEqual({'ConfigId': '2', 'ConfigName': 'Variable2', 'ConfigValue': 'TestE'},
                             indexPage.page.page.Nests['configSection'][0]['configItem'][1])

    def test_ShouldNotRememberNewItemNameOrValueAsExistingItems(self):
        indexPage = handlers.index.index((), {
            'configuration.Section1.Variable1': 'TestD',
            'configuration.Section1.Variable2': 'TestE',
            'configuration.Section2.Variable1': 'TestF',
            'configuration.Section2.NewItemName.1': 'Variable2',
            'configuration.Section2.NewItemValue.1': 'TestG'
        })

        indexPage.configuration.LoadFile = lambda filename: 0
        indexPage.configuration.config = \
            ConfigurationItem('', '', [
                ConfigurationItem('Section1', '', [
                    ConfigurationItem('variable1', 'TestA'),
                    ConfigurationItem('variable2', 'TestB')
                ]),
                ConfigurationItem('Section2', '', [
                    ConfigurationItem('variable3', 'TestC')
                ])
            ])

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
        indexPage.configuration.config = \
            ConfigurationItem('', '', [
                ConfigurationItem('Section1', '', [
                    ConfigurationItem('Variable1', 'TestA'),
                    ConfigurationItem('Variable2', 'TestB')
                ]),
                ConfigurationItem('Section2', '', [
                    ConfigurationItem('Variable1', 'TestC')
                ])
            ])

        indexPage.OutputPage()

        self.assertListEqual(
            [
                {'ConfigNumber': '1', 'ConfigName': 'Variable2', 'ConfigValue': 'TestG'}
            ],
            indexPage.page.page.Nests['configSection'][1]['newConfigItem'])

    def test_ShouldAddNewConfigurationSaveButtonPressed(self):
        indexPage = handlers.index.index((), {
            'configuration.Section1.Variable1': 'TestD',
            'configuration.Section1.Variable2': 'TestE',
            'configuration.Section2.Variable1': 'TestF',
            'configuration.Section2.NewItemName.1': 'Variable2',
            'configuration.Section2.NewItemValue.1': 'TestG',
            'submit': 'Save'
        })

        indexPage.SaveConfig = lambda: 0
        indexPage.OutputPage()

        self.assertDictEqual({}, indexPage.newConfigurationItems)
        self.assertListEqual(
            [ConfigurationItem('Variable1', 'TestF'), ConfigurationItem('Variable2', 'TestG')], 
            indexPage.configuration.config['Section2'].children
        )

    def test_ShouldDefaultToSimpleModeWhenNoModeSet(self):
        indexPage = handlers.index.index((), {})

        indexPage.OutputPage()

        self.assertFalse(indexPage.page.page.Nests['']['AdvancedMode'])

    def test_ShouldSetAdvancedModeWhenAdvancedButtonPressed(self):
        indexPage = handlers.index.index((), {'Mode': 'Advanced'})

        indexPage.OutputPage()

        self.assertTrue(indexPage.page.page.Nests['']['AdvancedMode'])

    def test_ShouldRememberCurrentStateWhenNonModeButtonPressed(self):
        indexPage = handlers.index.index((), {'CurrentMode': 'Advanced'})

        indexPage.OutputPage()

        self.assertTrue(indexPage.page.page.Nests['']['AdvancedMode'])