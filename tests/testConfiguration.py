import unittest
import cStringIO

import utils.Configuration


class TestConfiguration(unittest.TestCase):
    def setUp(self):
        self.configuration = utils.Configuration.Configuration()

    def test_ShouldPopulateSectionsWhenLoadFileCalled(self):
        iniContents = "[Section1]\n\n[Section2]\n\n[Section3]"
        iniStream = cStringIO.StringIO(iniContents)
        self.configuration.LoadStream(iniStream)
        self.assertDictEqual(self.configuration.config, {'Section1': {}, 'Section2': {}, 'Section3': {}})
        iniStream.close()

    def test_ShouldPopulateItemsWhenLoadFileCalled(self):
        iniContents = "[Section1]\nVariable1=TestA\nVariable2=TestB\n\n[Section2]\nVariable3=TestC\n\n[Section3]"
        iniStream = cStringIO.StringIO(iniContents)
        self.configuration.LoadStream(iniStream)
        self.assertDictEqual(self.configuration.config, {
            'Section1': {
                'variable1': 'TestA',
                'variable2': 'TestB'
            }, 'Section2': {
                'variable3': 'TestC'
            }, 'Section3': {

            }})
        iniStream.close()

    def test_ShouldWriteSectionsWhenSaveFileCalled(self):
        self.configuration.config = {'Section1': {}, 'Section2': {}, 'Section3': {}}

        iniStream = cStringIO.StringIO()
        self.configuration.WriteStream(iniStream)
        iniContents = iniStream.getvalue()
        iniStream.close()
        self.assertMultiLineEqual('[Section3]\n\n[Section2]\n\n[Section1]\n\n', iniContents)

    def test_ShouldWriteSectionsWhenSaveFileCalled(self):
        self.configuration.config = {
            'Section1': {
                'variable1': 'TestA',
                'variable2': 'TestB'
            }, 'Section2': {
                'variable3': 'TestC'
            }, 'Section3': {

            }}

        iniStream = cStringIO.StringIO()
        self.configuration.WriteStream(iniStream)
        iniContents = iniStream.getvalue()
        iniStream.close()
        self.assertMultiLineEqual(
            '''[Section3]\n\n[Section2]\nvariable3 = TestC\n\n[Section1]\nvariable1 = TestA\nvariable2 = TestB\n\n''',
            iniContents)