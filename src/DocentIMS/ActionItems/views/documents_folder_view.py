# -*- coding: utf-8 -*-

# from DocentIMS.ActionItems import _
from Products.Five.browser import BrowserView
from zope.interface import Interface

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
    
    def batch(self):
        # Retrieve the content listing with batching
        # batch = self.context.restrictedTraverse('@@contentlisting')(sort_on='sortable_title', batch=True, b_size=400)
        
        items = self.context.getFolderContents()
        
        return items

        # Initialize a dictionary to store items grouped by portal type
        grouped_items = {}

        # Loop through each item in the batch
        for item in items:
            # Get the portal type of the current item
            portal_t = item.portal_type

            # If this portal type isn't in the dictionary yet, add it with an empty list
            if portal_t not in grouped_items:
                grouped_items[portal_t] = []

            # Append the current item to the list for this portal type
            grouped_items[portal_t].append({title: item.Title()})

        # Return the grouped items dictionary
        return grouped_items
 
 