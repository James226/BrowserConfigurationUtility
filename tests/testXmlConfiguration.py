import unittest
import cStringIO
import utils


class TestXmlConfiguration(unittest.TestCase):
    def setUp(self):
        self.configuration = utils.Configuration.XmlConfiguration()

    def test_ShouldPopulateRootNodeWhenLoadStreamCalled(self):
        iniContents = '''<?xml version="1.0"?><rootNode></rootNode>'''
        iniStream = cStringIO.StringIO(iniContents)
        config = self.configuration.LoadStream(iniStream)
        self.assertDictEqual(config, {'rootNode': {}})
        iniStream.close()

    def test_ShouldPopulateNestedNodeWhenLoadStreamCalled(self):
        iniContents = '''<?xml version="1.0"?><rootNode><nestNode></nestNode></rootNode>'''
        iniStream = cStringIO.StringIO(iniContents)
        config = self.configuration.LoadStream(iniStream)
        self.assertDictEqual(config, {'rootNode': {'nestNode': {}}})
        iniStream.close()

    def test_ShouldPopulateNodeTextWhenLoadStreamCalled(self):
        iniContents = '''<?xml version="1.0"?><rootNode><nestNode>Text</nestNode></rootNode>'''
        iniStream = cStringIO.StringIO(iniContents)
        config = self.configuration.LoadStream(iniStream)
        self.assertDictEqual(config, {'rootNode': {'nestNode': {'Value': 'Text'}}})
        iniStream.close()

    def test_ShouldPopulateAttributesWhenLoadStreamCalled(self):
        iniContents = '''<?xml version="1.0"?><rootNode><nestNode attribute1="TestA" attribute2="TestB">Text</nestNode></rootNode>'''
        iniStream = cStringIO.StringIO(iniContents)
        config = self.configuration.LoadStream(iniStream)
        self.assertDictEqual(config, {
            'rootNode': {
                'nestNode': {
                    'Attributes': {
                        'attribute1': 'TestA',
                        'attribute2': 'TestB'
                    },
                    'Value': 'Text'
                }}})
        iniStream.close()