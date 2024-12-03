# -*- coding: utf-8 -*-

# from DocentIMS.ActionItems import _
from Acquisition import aq_inner
from Products.Five.browser import BrowserView
from zope.interface import Interface
from plone.app.contenttypes.behaviors.collection import ICollection
from Products.CMFCore.utils import getToolByName
from plone import api
from plone.base.batch import Batch
 
class IDocumentsFolderView(Interface):
    """ Marker Interface for IDocumentsFolderView"""


class DocumentsFolderView(BrowserView):
    #b_size = 25
    
    def __call__(self):
        return self.index()
    
    @property
    def collection_behavior(self):
        return ICollection(aq_inner(self.context))

    @property
    def b_size(self):
        # import pdb; pdb.set_trace()
        if self.context.Type() == 'Collection':
            return getattr(self, "_b_size", self.collection_behavior.item_count)
        return getattr(self, "_b_size", 25)
    
    def get_types(self):
        meeting_types = self.context.portal_catalog.uniqueValuesFor("meeting_type")
        return sorted(meeting_types)
 
    
    def batch(self, mtype):
        b_start_str = f"b_start_{mtype}"
        b_start = self.request.get(b_start_str, 0)
        b_size = self.b_size
        listing = self.context.restrictedTraverse("@@contentlisting")
        items = listing(batch=False, meeting_type=mtype)
        return Batch(
            items,
            b_size,
            b_start,
            b_start_str=b_start_str,
        )
            
        