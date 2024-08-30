# -*- coding: utf-8 -*-

# from DocentIMS.ActionItems import _
from Products.Five.browser import BrowserView
from zope.interface import Interface
from Products.CMFCore.utils import getToolByName
from plone import api
from plone.base.batch import Batch

# from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile


class IDocumentsFolderView(Interface):
    """ Marker Interface for IDocumentsFolderView"""


class DocumentsFolderView(BrowserView):
    # template = ViewPageTemplateFile('documents_folder_view.pt')

    b_size = 25
    
    def __call__(self):
        return self.index()
    
    def get_types(self):
        view = self.context.restrictedTraverse("@@contentlisting")
        ptypes = set()
        for it in view(batch=False):
            ptypes.add(it.portal_type)
        return sorted(ptypes)

    def batch(self, ptype):
        b_start_str = f"b_start_{ptype}"
        b_start = self.request.get(b_start_str, 0)
        listing = self.context.restrictedTraverse("@@contentlisting")
        items = listing(batch=False, portal_type=ptype)
        return Batch(
            items,
            self.b_size,
            b_start,
            b_start_str=b_start_str,
        )
            
        