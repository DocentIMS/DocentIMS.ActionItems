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
        colors = ['#CCCCCC',  '#FF0000',  'orange', '#123456']
        today = datetime.date.today()
        now = datetime.datetime.now(timezone.utc)
        items = items = self.batch()

        itemlist = []
        index = 0
        #contentitems = [item[1] for item in items]

        for item in items:
            if item.portal_type == 'action_items':
                title = item.Title()
                duedate = item.duedate or today
                created = item.created
                delta = duedate - today
                delta2 =  now -  created.asdatetime()
                #delta3 =  duedate -  created.asdatetime()
                itemlist.append({'title': title, 'data': [delta2.days, delta.days], 'index': index})
                index += 1

        #import pdb; pdb.set_trace()
        return itemlist
