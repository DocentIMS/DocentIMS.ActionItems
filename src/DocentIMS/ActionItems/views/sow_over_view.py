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




class SowOverView(BrowserView):

    def __call__(self):
        #self.msg = _(u'A small message')
        return self.index()


    def batch(self):
        batch = self.context.restrictedTraverse('@@contentlisting')(sort_on='sortable_title', batch=True, b_size=400);
        return batch

    def get_fields(self):
        return api.portal.get_registry_record('scope_table_columns', interface=IDocentimsSettings)
    
    @property
    def portal_url(self):
        return api.portal.get().absolute_url() 
 

    def today(self):
        #import pdb; pdb.set_trace()
        return datetime.date.today()

    


class SowCollectionView(CollectionView, SowOverView):

    def __call__(self):
        return self.index()
