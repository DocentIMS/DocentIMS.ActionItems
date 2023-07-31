# -*- coding: utf-8 -*-

from DocentIMS.ActionItems import _
from Products.Five.browser import BrowserView
from plone import api
from ..interfaces import IDocentimsSettings
import DateTime
import datetime
# from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile


class ActionItemsOverView(BrowserView):

    def __call__(self):
        #self.msg = _(u'A small message')
        return self.index()

    def get_fields(self):
        return api.portal.get_registry_record('table_columns', interface=IDocentimsSettings)

    def today(self):
        #import pdb; pdb.set_trace()
        return datetime.date.today()
