# -*- coding: utf-8 -*-

# from DocentIMS.ActionItems import _
from Products.Five.browser import BrowserView
from zope.interface import Interface

# from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile


class IMeetingNotesView(Interface):
    """ Marker Interface for IMeetingNotesView"""


class MeetingNotesView(BrowserView):
    # If you want to define a template here, please remove the template from
    # the configure.zcml registration of this view.
    # template = ViewPageTemplateFile('meeting_notes_view.pt')

    def __call__(self):
        # Implement your own actions:
        return self.index()
