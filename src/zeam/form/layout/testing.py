

import zeam.form.layout
from grokcore.component import zcml
from zope.app.wsgi.testlayer import BrowserLayer
from zope.configuration.config import ConfigurationMachine

import zope.testbrowser.wsgi


class Layer(
        zope.testbrowser.wsgi.TestBrowserLayer,
        BrowserLayer):
    pass


FunctionalLayer = Layer(zeam.form.layout, allowTearDown=True)


def grok(module_name):
    config = ConfigurationMachine()
    zcml.do_grok(module_name, config)
    config.execute_actions()
