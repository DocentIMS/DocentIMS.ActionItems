# -*- coding: utf-8 -*-

from DocentIMS.ActionItems import _
from Products.Five.browser import BrowserView
from plone import api
from ..interfaces import IDocentimsSettings

# from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile


class ActionItemsOverView(BrowserView):

    def __call__(self):
        #self.msg = _(u'A small message')
        return self.index()

    def get_fields(self):
        #import pdb; pdb.set_trace()
        return api.portal.get_registry_record('table_columns', interface=IDocentimsSettings)



        #if items:
        #    terms = [ SimpleTerm(value=item.UID, token=item.UID, title=item.Title) for item in items ]
        #    return SimpleVocabulary(terms)
        #return SimpleVocabulary([])
