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