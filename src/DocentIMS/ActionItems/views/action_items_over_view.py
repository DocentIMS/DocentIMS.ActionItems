# -*- coding: utf-8 -*-

from DocentIMS.ActionItems import _
from Products.Five.browser import BrowserView
from plone import api
from ..interfaces import IDocentimsSettings
import DateTime
import datetime
from datetime import timezone
# from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile


from Acquisition import aq_inner
from plone.batching import Batch
from zope.component import getMultiAdapter
from zope.component import getUtility
#import plone.api

from plone.app.contenttypes.browser.collection import CollectionView




class ActionItemsOverView(BrowserView):

    def __call__(self):
        #self.msg = _(u'A small message')
        return self.index()


    def batch(self):
        batch = self.context.restrictedTraverse('@@contentlisting')(sort_on='sortable_title', batch=True, b_size=400);
        return batch

    def get_fields(self):
        return api.portal.get_registry_record('table_columns', interface=IDocentimsSettings)

    def today(self):
        #import pdb; pdb.set_trace()
        return datetime.date.today()

    def get_graphdata(self):
        colors = ['#CCCCCC',  '#FF0000',  'orange', '#123456']

        #if self.context.portal_type=="Collection":
        items = self.batch()
        #else:
        #    items =  self.context.items()

        datanames = []
        datavalues  = []
        datacolors = []
        for item in items:
            if item.portal_type == 'action_items':
                datanames.append(item.Title())

                if item.priority:
                    datavalues.append(item.priority)
                    datacolors.append(colors[item.priority])
                else:
                    datacolors.append('#CCCCCC')
                    datavalues.append(0)
        return datanames, datavalues, datacolors


    def get_piedata(self):
        colors = ['#FF0000',  'orange', '#123456']
        items = items = self.batch()

        priority1 = 0
        priority2 = 0
        priority3 = 0

        for item in items:
            if item.portal_type == 'action_items':

                if item.priority == 3:
                    priority3 += 1
                if item.priority == 2:
                    priority2 += 1
                if item.priority == 1:
                    priority1 += 1



        return [[ priority1, priority2, priority3  ], ['#FF0000',  'orange', '#123456']]




class ActionItemsCollectionView(CollectionView, ActionItemsOverView):

    def __call__(self):
        return self.index()

    def get_graphdata(self):
        #colors = """'#FF0000',  'orange', '#123456'"""

        items = self.batch()

        priority1 = 0
        priority2 = 0
        priority3 = 0

        #datavalues  = []
        #datacolors = []
        for item in items:
            if item.portal_type == 'action_items':

                if item.priority == 3:
                    priority3 += 1
                if item.priority == 2:
                    priority2 += 1
                if item.priority == 1:
                    priority1 += 1

        datanames = ['Priority 1: ' +  str(priority1) + ' item(s)', 'Priority 2: ' +  str(priority2)  + ' item(s)', 'Priority 3: ' +  str(priority3)  + ' item(s)']
        #datanames = ['Priority 1: '  , 'Priority 2: '   , 'Priority 3: '   ]

        return  [priority1, priority2, priority3 ]
