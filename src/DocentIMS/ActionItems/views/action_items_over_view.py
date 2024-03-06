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
from Products.CMFCore.utils import getToolByName
from plone.app.contenttypes.browser.collection import CollectionView




class ActionItemsOverView(BrowserView):

    def __call__(self):
        #self.msg = _(u'A small message')
        return self.index()
    
    #def portal_url(self):
    #    return api.portal.get().absolute_url()

    def batch(self):
        batch = self.context.restrictedTraverse('@@contentlisting')(sort_on='sortable_title', batch=True, b_size=400);
        return batch

    def get_fields(self):
        return api.portal.get_registry_record('table_columns', interface=IDocentimsSettings)
    
    @property
    def portal_url(self):
        return api.portal.get().absolute_url() 
 
    ##@property
    def xuid_title(self, val):
        if val:
            uid_object =  api.content.get(UID=val) 
            return uid_object.Title()
        return ''

    def uid_title(context, uuid):
        catalog = getToolByName(context, 'portal_catalog')
        results = catalog(UID=uuid)
        if results:
            return results[0].Title
        else:
            return ''

    
    def today(self):
        #import pdb; pdb.set_trace()
        return datetime.date.today()

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

                if item.priority:

                    if item.priority == 3:
                        priority3 += 1
                    if item.priority == 2:
                        priority2 += 1
                    if item.priority == 1:
                        priority1 += 1

        datanames = ['Priority 1: ' +  str(priority1) + ' item(s)', 'Priority 2: ' +  str(priority2)  + ' item(s)', 'Priority 3: ' +  str(priority3)  + ' item(s)']
        #datanames = ['Priority 1: '  , 'Priority 2: '   , 'Priority 3: '   ]

        return  [datanames, [priority1, priority2, priority3]]


    def get_piedata(self):
        #colors = ['#FF0000',  'orange', '#123456']
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


        return [ priority1, priority2, priority3 ]


    def get_urgencydata(self):
        #colors = """'#FF0000',  'orange', '#123456'"""

        items = self.batch()

        red = api.portal.get_registry_record('urgent_red', interface=IDocentimsSettings)
        yellow = api.portal.get_registry_record('soon_yellow', interface=IDocentimsSettings)
        green = api.portal.get_registry_record('future_green', interface=IDocentimsSettings)
        
        urgent = "Urgent < {days} workdays".format(days = red)
        soon = "Soon < {days} workdays".format(days = yellow) 
        future = "Future < {days} workdays".format(days = green) 
        more = 'More than {days}'.format(days = green)  

        urgency1 = 0
        urgency2 = 0
        urgency3 = 0
        urgency4 = 0

        #leftdays  = []
        #datacolors = []
        for item in items:
            if item.portal_type == 'action_items':
                if item.urgency:
                    if item.urgency == urgent:
                        urgency1 += 1

                    if item.urgency == soon:
                        urgency2 += 1

                    if item.urgency == future:
                        urgency3 += 1

                    if item.urgency == more:
                        urgency4 += 1
 

        #datanames = [urgent + ' item(s)', soon  + ' item(s)', future  + ' item(s)', more  + ' item(s)']
        datanames = ["< {} days'".format(red), "< {} + days'".format(yellow), "< {}  days'".format(green), 'more']
        
        return  [datanames, [urgency1, urgency2, urgency3, urgency4]]


class ActionItemsCollectionView(CollectionView, ActionItemsOverView):

    def __call__(self):
        return self.index()
