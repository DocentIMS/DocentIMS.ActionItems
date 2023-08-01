# -*- coding: utf-8 -*-

from DocentIMS.ActionItems import _
from Products.Five.browser import BrowserView
from plone import api
from ..interfaces import IDocentimsSettings
import DateTime
import datetime
from datetime import timezone
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

    def get_graphdata(self):
        colors = ['#CCCCCC',  '#FF0000',  'orange', '#123456']
        items = self.context.items()
        datanames = [item[1].Title() for item in items]
        datavalues = [item[1].priority if hasattr(item[1], 'priority') else 0 for item in items]
        datacolors = [ colors[datavalue] if datavalue != None else '#CCCCCC' for datavalue in datavalues]
        return datanames, datavalues, datacolors


    def get_piedata(self):
        colors = ['#CCCCCC',  '#FF0000',  'orange', '#123456']
        today = datetime.date.today()
        now = datetime.datetime.now(timezone.utc)
        items = self.context.items()

        itemlist = []
        index = 0
        contentitems = [item[1] for item in items]

        for item in contentitems:
            title = item.Title()
            duedate = item.duedate or today
            created = item.created()
            delta = duedate - today
            delta2 =  now -  created.asdatetime()
            #delta3 =  duedate -  created.asdatetime()
            itemlist.append({'title': title, 'data': [delta.days, delta2.days], 'index': index})
            index += 1

        #import pdb; pdb.set_trace()
        return itemlist
