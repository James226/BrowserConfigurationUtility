import unittest

import handlers.index


class TestIndex(unittest.TestCase):
    def test_canParseHTML(self):
        indexPage = handlers.index.index((), {})
        indexPage.OutputPage()

        self.assertEqual(indexPage.page.page.Nests['']['ConfigFilename'], 'SampleIniFile.ini')