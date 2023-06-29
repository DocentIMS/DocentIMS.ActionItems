# -*- coding: utf-8 -*-

# from DocentIMS.ActionItems import _
from Products.Five.browser import BrowserView
from zope.interface import Interface
from plone import api
import DateTime
import datetime

# from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile


class IActionItemsView(Interface):
    """ Marker Interface for IActionItemsView"""


class ActionItemsView(BrowserView):
    # If you want to define a template here, please remove the template from
    # the configure.zcml registration of this view.
    # template = ViewPageTemplateFile('action_items_view.pt')

    def __call__(self):
        # Implement your own actions:
        return self.index()

    def portal_url(self):
        return api.portal.get().absolute_url()

    def due_date(self):
        return self.context.created().ISO()
        #return datetime.datetime.from_date(initial_due_date).ISO()
        #return self.context.initial_due_date().ISO()
