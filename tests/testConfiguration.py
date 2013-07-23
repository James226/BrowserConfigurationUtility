import unittest
import cStringIO

import utils.Configuration

from utils.Configuration import ConfigurationItem

class TestConfiguration(unittest.TestCase):
    def setUp(self):
        self.configuration = utils.Configuration.IniConfiguration()

    def test_ShouldPopulateSectionsWhenLoadFileCalled(self):
        iniContents = "[Section1]\n\n[Section2]\n\n[Section3]"
        iniStream = cStringIO.StringIO(iniContents)
        config = self.configuration.LoadStream(iniStream)
        self.assertEquals(config, ConfigurationItem('', '', [ConfigurationItem('Section1', ''), ConfigurationItem('Section2', ''), ConfigurationItem('Section3', '')]))
        iniStream.close()

    def test_ShouldPopulateItemsWhenLoadFileCalled(self):
        self.maxDiff = None
        iniContents = "[Section1]\nvariable1=TestA\nvariable2=TestB\n\n[Section2]\nvariable3=TestC\n\n[Section3]"
        iniStream = cStringIO.StringIO(iniContents)
        config = self.configuration.LoadStream(iniStream)
        self.assertEquals(config,
            ConfigurationItem('', '', [
                ConfigurationItem('Section1', '', 
                    [
                        ConfigurationItem('variable1', 'TestA'),
                        ConfigurationItem('variable2', 'TestB')
                    ]),
                ConfigurationItem('Section2', '', 
                    [
                        ConfigurationItem('variable3', 'TestC')
                    ]),
                ConfigurationItem('Section3', '')
            ]))
        iniStream.close()

    def test_ShouldWriteSectionsWhenSaveFileCalled(self):
        config = \
            ConfigurationItem('', '', [
                ConfigurationItem('Section1', ''),
                ConfigurationItem('Section2', ''),
                ConfigurationItem('Section3', '')
            ])

        iniStream = cStringIO.StringIO()
        self.configuration.WriteStream(iniStream, config)
        iniContents = iniStream.getvalue()
        iniStream.close()
        self.assertMultiLineEqual('[Section1]\n\n[Section2]\n\n[Section3]\n\n', iniContents)

    def test_ShouldWriteItemsWhenSaveFileCalled(self):
        config = \
            ConfigurationItem('', '', [
                ConfigurationItem('Section1', '', [
                    ConfigurationItem('variable1', 'TestA'),
                    ConfigurationItem('variable2', 'TestB')
                ]),
                ConfigurationItem('Section2', '', [
                    ConfigurationItem('variable3', 'TestC'),
                ]),
                ConfigurationItem('Section3', '')
            ])

        iniStream = cStringIO.StringIO()
        self.configuration.WriteStream(iniStream, config)
        iniContents = iniStream.getvalue()
        iniStream.close()
        self.assertMultiLineEqual(
            '''[Section1]\nvariable1 = TestA\nvariable2 = TestB\n\n[Section2]\nvariable3 = TestC\n\n[Section3]\n\n''',
            iniContents)
    
    def test_ShouldRemoveItemWhenDeleteChildCalled(self):
        config = \
            ConfigurationItem('', '', [
                ConfigurationItem('Section1', '', [
                    ConfigurationItem('variable1', 'TestA'),
                    ConfigurationItem('variable2', 'TestB')
                ]),
                ConfigurationItem('Section2', '', [
                    ConfigurationItem('variable3', 'TestC'),
                ]),
                ConfigurationItem('Section3', '')
            ])

        config.DeleteChild('Section1')

        self.assertListEqual([ConfigurationItem('Section2', '', [
                    ConfigurationItem('variable3', 'TestC'),
                ]),
                ConfigurationItem('Section3', '')], config.children)