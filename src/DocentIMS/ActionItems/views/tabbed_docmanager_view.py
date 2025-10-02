# -*- coding: utf-8 -*-

# from DocentIMS.ActionItems import _
from Products.Five.browser import BrowserView
from zope.interface import Interface
from collections import defaultdict
from Missing import Value as MissingValue

# from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile


class ITabbedDocmanagerView(Interface):
    """ Marker Interface for ITabbedDocmanagerView"""


class TabbedDocmanagerView(BrowserView):
    # If you want to define a template here, please remove the template from
    # the configure.zcml registration of this view.
    # template = ViewPageTemplateFile('tabbed_documents_view.pt')

    def __call__(self):
        # Implement your own actions:
        return self.index()
    
    def grouped_items_by_document_type(self):
        """Return items in current folder grouped by document_type index."""
        context = self.context
        catalog =  context.portal_catalog
        
        # Get brains for items in *this folder only*
        brains = catalog(
            path={'query': '/'.join(context.getPhysicalPath()), 'depth': 1}
        )
        
        groups = defaultdict(list)
        
        for brain in brains:
            doc_type = getattr(brain, 'document_type', None)  # index value
            if doc_type is None or doc_type is MissingValue:
                doc_type = "Unknown"
            obj = brain.getObject()
            groups[doc_type].append(obj)
        
        # Convert to list of dicts (to preserve your requested format)
        # And sort them
        return [
                {"document_type": doc_type, "items": items}
                for doc_type, items in sorted(groups.items(), key=lambda x: (x[0] or "").lower())
            ]
        
        # return returnlist
