# -*- coding: utf-8 -*-

# from DocentIMS.ActionItems import _
from Products.Five.browser import BrowserView
from zope.interface import Interface

# from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile


class IReindexView(Interface):
    """ Marker Interface for IProjectView"""


class ReindexView(BrowserView):
    # If you want to define a template here, please remove the template from
    # the configure.zcml registration of this view.
    # template = ViewPageTemplateFile('project_view.pt')

    def __call__(self):
        # Implement your own actions:
        return self.reindex()

    def reindex(self):
        my_brains = self.context.portal_catalog(portal_type=['action_items'])
        for brain in my_brains:
            brain.getObject().reindexObject(idxs=["daysleft"])
        
        return len(my_brains)
