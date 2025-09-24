# -*- coding: utf-8 -*-

# from DocentIMS.ActionItems import _
from Acquisition import aq_inner
from Products.Five.browser import BrowserView
from zope.interface import Interface
from plone.app.contenttypes.behaviors.collection import ICollection
from Products.CMFCore.utils import getToolByName
from plone import api
from plone.base.batch import Batch

# from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile


class IDocumentsFolderView(Interface):
    """ Marker Interface for IDocumentsFolderView"""


class DocumentsFolderView(BrowserView):
    # template = ViewPageTemplateFile('documents_folder_view.pt')

    #b_size = 25
    
    
    def __call__(self):
        return self.index()
    
    @property
    def collection_behavior(self):
        return ICollection(aq_inner(self.context))

    @property
    def b_size(self):
          
        if self.context.Type() == 'Collection':
            return getattr(self, "_b_size", self.collection_behavior.item_count)
        return getattr(self, "_b_size", 25)
    
    def get_types(self):
        view = self.context.restrictedTraverse("@@contentlisting")
        ptypes = set()
        for it in view(batch=False):
            ptypes.add(it.portal_type)
        if 'Folder' in ptypes:
            ptypes.remove("Folder")
        return sorted(ptypes)
    
    def get_folder_content(self, uid):
        b_start_str = f"b_start"
        # b_size = self.request.get(b_size, 25)
        b_size = self.b_size
        b_start = self.request.get(b_start_str, 0)
        folder = api.content.get(UID=uid)
        listing = api.content.get_view(name="contentlisting", context=folder)
        
        items = listing(batch=False)
        return Batch(
            items,
            b_size,
            b_start,
            b_start_str=b_start_str,
        )
    
    def batch(self, ptype):
        b_start_str = f"b_start_{ptype}"
        b_start = self.request.get(b_start_str, 0)
        b_size = self.b_size
        listing = self.context.restrictedTraverse("@@contentlisting")
        items = listing(batch=False, portal_type=ptype)
        return Batch(
            items,
            b_size,
            b_start,
            b_start_str=b_start_str,
        )
            
        