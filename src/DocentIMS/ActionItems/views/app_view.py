# -*- coding: utf-8 -*-

# from DocentIMS.ActionItems import _
from Products.Five.browser import BrowserView
from zope.interface import Interface
# from Products.CMFCore.utils import getToolByName

# from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile


class IAppView(Interface):
    """ Marker Interface for IAppView"""


class AppView(BrowserView):
    # If you want to define a template here, please remove the template from
    # the configure.zcml registration of this view.
    # template = ViewPageTemplateFile('app_view.pt')

    def __call__(self):
        # Implement your own actions:
        return self.index()
    
    def len_ais(self):
        my_brains = self.context.portal_catalog(portal_type=['action_items'])
        
        if my_brains:        
            return len(my_brains)
    
    def count_ais(self):
        urgencies = self.context.portal_catalog.uniqueValuesFor("urgency")
        if urgencies:
            urgency_list = []
            for urgency in urgencies:
                my_brains = self.context.portal_catalog(portal_type=['action_items'], urgency=urgency)
                urgency_list.append({'name': urgency, 'count': len(my_brains)})
            return urgency_list
            
        return None


    def len_meetings(self):
        # urgencies = self.context.portal_catalog.uniqueValuesFor("meeting_types")
        my_brains = self.context.portal_catalog(portal_type=['meeting', 'Meeting'] )
        return len(my_brains)
        # return None
        
    def count_meetings(self):
        meeting_types = self.context.portal_catalog.uniqueValuesFor("meeting_type")
        if meeting_types:
            meeting_list = []
            for meeting_type in meeting_types:
                my_brains = self.context.portal_catalog(portal_type=['meeting', 'Meeting'], meeting_type=meeting_type)
                meeting_list.append({'name': meeting_type, 'count': len(my_brains)})
            return meeting_list
            
        return None