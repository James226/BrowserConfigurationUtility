import unittest

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

