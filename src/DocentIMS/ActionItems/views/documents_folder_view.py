# -*- coding: utf-8 -*-

# from DocentIMS.ActionItems import _
from Products.Five.browser import BrowserView
from zope.interface import Interface
from Products.CMFCore.utils import getToolByName
from plone import api

# from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile


class IDocumentsFolderView(Interface):
    """ Marker Interface for IDocumentsFolderView"""


class DocumentsFolderView(BrowserView):
    # If you want to define a template here, please remove the template from
    # the configure.zcml registration of this view.
    # template = ViewPageTemplateFile('documents_folder_view.pt')

    def __call__(self):
        # Implement your own actions:
        return self.index()
    
    
    # def batch(self):
    #     batch = self.context.restrictedTraverse('@@contentlisting')(sort_on='sortable_title', batch=True, b_size=400);
    #     return batch
    
    def get_types(self):
        folder = self.context  # Assuming the script is created inside the folder
        portal_types = [item.portal_type for item in folder.objectValues()]

        return sorted(set(portal_types))
        
    def batch(self, contentype):
        batch = self.context.restrictedTraverse('@@contentlisting')(sort_on='sortable_title',  portal_type=contentype, batch=True, b_size=400)
        return batch
 
 