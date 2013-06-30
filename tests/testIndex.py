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

        def saveConfiguration(config):
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
                'Variable1': 'TestA',
                'Variable2': 'TestB'
            }, 'Section2': {
                'Variable3': 'TestC'
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


