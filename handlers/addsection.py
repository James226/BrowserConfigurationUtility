from Giraffe.template import template


class AddSection(object):
    def __init__(self, args, kw):
        self.args = args
        self.kwargs = kw

    def OutputPage(self):
        if 'filename' not in self.kwargs:
            self.filename = "SampleIniFile.ini"
        else:
            self.filename = self.kwargs['filename']

        self.page = template.Load("addsection")
        self.page.SetVariable("ConfigFilename", self.filename)

        return self.page.OutputPage()