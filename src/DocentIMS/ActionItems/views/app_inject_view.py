# -*- coding: utf-8 -*-

# from DocentIMS.ActionItems import _
from Products.Five.browser import BrowserView
from zope.interface import Interface

# from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile


class IAppInjectView(Interface):
    """ Marker Interface for IAppInjectView"""


class AppInjectView(BrowserView):
    # If you want to define a template here, please remove the template from
    # the configure.zcml registration of this view.
    # template = ViewPageTemplateFile('app_inject_view.pt')

    def __call__(self):
        # Implement your own actions:
        return self.index()
