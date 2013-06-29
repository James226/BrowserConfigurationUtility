import ConfigParser
import os
import re

import cherrypy

from Giraffe.template import *


class WebServer:
    @cherrypy.expose
    def index(self, filename="SampleIniFile.ini"):
        indexPage = template.Load("index")
        indexPage.SetVariable("ConfigFilename", filename)

        completeFilename = 'config/' + filename
        if re.match("([a-zA-Z0-9\-_ \(\)]+)\.([a-zA-Z0-9\-_]+)", filename) is None or not os.path.exists(
                completeFilename):
            return 'Invalid filename specified: ' + filename

        for configFilename in os.listdir('config/'):
            indexPage.AddNest('fileTab', {
                'Selected': True if (configFilename == filename) else False,
                'Filename': configFilename
            })

        config = ConfigParser.ConfigParser()
        config.readfp(open(completeFilename))
        for section in config.sections():
            sectionNest = indexPage.AddNest("configSection", {
                'SectionName': section
            })
            for (configName, configValue) in config.items(section):
                indexPage.AddSubNest(sectionNest, "configItem", {
                    'ConfigName': configName,
                    'ConfigValue': configValue
                })

        return indexPage.OutputPage()

    @cherrypy.expose
    def saveConfig(self, *args, **kw):
        configuration = {}
        for (name, value) in kw.items():
            nameParts = name.split('.')
            if len(nameParts) == 3:
                if nameParts[0] == 'configuration':
                    if not nameParts[1] in configuration:
                        configuration[nameParts[1]] = {}
                    configuration[nameParts[1]][nameParts[2]] = value

        completeFilename = 'config/' + kw['filename']
        if re.match("([a-zA-Z0-9\-_ \(\)]+)\.([a-zA-Z0-9\-_]+)", kw['filename']) is None or not os.path.exists(
                completeFilename):
            return 'Invalid filename specified: ' + kw['filename']

        config = ConfigParser.ConfigParser()
        with open(completeFilename, 'r') as fp:
            config.readfp(fp)
            for (section, configItems) in configuration.items():
                for (name, value) in configItems.items():
                    config.set(section, name, value)

        with open(completeFilename, 'w') as fp:
            config.write(fp)

        return self.index(kw['filename'])


settings = os.path.join(os.path.dirname(__file__), 'settings.conf')

if __name__ == '__main__':
    # CherryPy always starts with app.root when trying to map request URIs
    # to objects, so we need to mount a request handler root. A request
    # to '/' will be mapped to HelloWorld().index().
    cherrypy.quickstart(WebServer(), config=settings)
else:
    # This branch is for the test suite; you can ignore it.
    cherrypy.tree.mount(WebServer(), config=settings)
