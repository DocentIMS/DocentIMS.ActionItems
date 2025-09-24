# -*- coding: utf-8 -*-

# from DocentIMS.ActionItems import _
from Products.Five.browser import BrowserView
from zope.interface import Interface

# from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile


class IMinutesView(Interface):
    """ Marker Interface for IMinutesView"""


class MinutesView(BrowserView):
    # If you want to define a template here, please remove the template from
    # the configure.zcml registration of this view.
    # template = ViewPageTemplateFile('minutes_view.pt')

    def __call__(self):
        # Implement your own actions:
        return self.index()
    
    def filename(self):
          
        my_file = self.context.file
        if my_file and my_file != None:
            return my_file.filename
        return ''