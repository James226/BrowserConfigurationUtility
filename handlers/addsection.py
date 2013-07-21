import re
import os

from Giraffe.template import template

import utils.Configuration


class AddSection(object):
    def __init__(self, args, kw):
        self.args = args
        self.kwargs = kw
        self.error = ''
        self.configPath = 'config/'
        self.filename = ''

    def _SaveSection(self):

        config = utils.Configuration.Configuration()

        self.completeFilename = self.configPath + self.filename
        if self.isValidFilename(self.filename) or not os.path.exists(self.completeFilename):
            self.error = 'Invalid filename specified: ' + self.filename
            return False

        config.LoadFile(self.completeFilename)

        if self.kwargs['sectionName'] == '':
            self.error = 'No section name specified'
            return False

        if self.kwargs['sectionName'] in config.config:
            self.error = 'Specified section name already exists'
            return False

        if self.kwargs['sectionName'] not in config.config:
            config.config.AddChild(utils.Configuration.ConfigurationItem(self.kwargs['sectionName'], ''))
        
        config.WriteFile(self.completeFilename)

        return True

    def isValidFilename(self, filename):
        return re.match("([a-zA-Z0-9\-_ \(\)]+)\.([a-zA-Z0-9\-_]+)", filename) is None

    def OutputPage(self):
        if 'filename' not in self.kwargs:
            self.filename = "SampleIniFile.ini"
        else:
            self.filename = self.kwargs['filename']

        if 'sectionName' not in self.kwargs:
            self.kwargs['sectionName'] = ''

        if 'saveSection' in self.kwargs:
            if self._SaveSection():
                return '<script>window.location = "/";</script>'

        self.page = template.Load("addsection")

        self.page.SetVariable("ConfigFilename", self.filename)
        self.page.SetVariable("SectionName", self.kwargs['sectionName'])

        if self.error is not '':
            self.page.SetVariable('errorBlock', True)
            self.page.SetVariable('ErrorMessage', self.error)

        return self.page.OutputPage()