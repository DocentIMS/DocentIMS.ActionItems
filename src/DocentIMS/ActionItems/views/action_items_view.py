# -*- coding: utf-8 -*-

# from DocentIMS.ActionItems import _
from Products.Five.browser import BrowserView
from zope.interface import Interface
from plone import api
import DateTime
import datetime


class IActionItemsView(Interface):
    """ Marker Interface for IActionItemsView"""


class ActionItemsView(BrowserView):

    def portal_url(self):
        return api.portal.get().absolute_url()

    def due_date(self):
        return self.context.created().ISO()
        #return datetime.datetime.from_date(initial_due_date).ISO()
        #return self.context.initial_due_date().ISO()

    def source_relations(self):
        relations =  api.relation.get(source=self.context)
        return relations

    def target_relations(self):
        relations =  api.relation.get(target=self.context)
        return relations
