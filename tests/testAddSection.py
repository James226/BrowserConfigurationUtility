import os
import unittest

import utils.Configuration
from utils.Configuration import ConfigurationItem
from handlers import addsection


class testAddSection(unittest.TestCase):
    def test_ShouldDefaultSectionNameToEmptyString(self):
        page = addsection.AddSection((), {})
        page.OutputPage()
        self.assertEqual('', page.page.page.Nests['']['SectionName'])

    def test_ShouldUseFilenameGiven(self):
        page = addsection.AddSection((), {
            'filename': 'test.ini'
        })
        page.OutputPage()
        self.assertEqual('test.ini', page.page.page.Nests['']['ConfigFilename'])

    def test_ShouldSaveSectionWhenSaveClicked(self):
        global sectionSaved
        sectionSaved = False

        def SaveSection():
            global sectionSaved
            sectionSaved = True

        page = addsection.AddSection((), {'saveSection': 'Value'})
        page._SaveSection = SaveSection
        page.OutputPage()
        self.assertTrue(sectionSaved)

    def test_ShouldAddNewSectionToConfigurationWhenSaveSectionCalled(self):
        global config
        config = None
        def TrueFunc(var1=None):
            return True

        def FalseFunc(var1=None):
            return False

        def LoadConfig(inst, filename):
            inst.config = ConfigurationItem('', '')
            

        def CaptureConfig(inst, filename):
            global config
            config = inst.config

        page = addsection.AddSection((), {'sectionName': 'NewSection', 'saveSection': 'Value'})
        page.isValidFilename = FalseFunc
        pathExists = os.path.exists
        os.path.exists = TrueFunc
        utils.Configuration.Configuration.LoadFile = LoadConfig
        utils.Configuration.Configuration.WriteFile = CaptureConfig
        
        page._SaveSection()

        os.path.exists = pathExists

        self.assertEqual(config, ConfigurationItem('', '', [ConfigurationItem('NewSection', '')]))


