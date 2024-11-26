# -*- coding: utf-8 -*-

# from DocentIMS.ActionItems import _
from Products.Five.browser import BrowserView
from zope.interface import Interface
import requests
from plone import api
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

        
    def get_buttons(self):
        urls = ["https://mymeadows.org", "http://mymeadows.org:8084/Plone_24_10_24"]
        buttons = []
        
        for siteurl in urls:
            response = requests.get(f'{siteurl}/@item_count?user={self.get_current()}', headers={'Accept': 'application/json', 'Content-Type': 'application/json'},  auth=('admin', 'admin'))
            if response:
                body = response.json()
                buttons.append({'name': body['dashboard-list']['short_name'], 'url': siteurl, 'project_color': body['dashboard-list']['project_color']})
        
        return buttons
    
    def get_current(self):
        current = api.user.get_current()
        #return current.getId()
        return current.getProperty('email')
 

    def get_dashboard_info(self):
        # Change to own api endpoint
        # response = requests.get('http://ubuntu.local:8605/Plone14/@search', headers={'Accept': 'application/json', 'Content-Type': 'application/json'},  auth=('admin', 'admin'))
        
        # TO DO, change admin
        
        #******
        #******
        #******
        #******
        #******
        #******
        
        request = self.request
        siteurl = self.request.siteurl
        user = self.get_current()
        
        response = requests.get(f'{siteurl}/@item_count?user={user}', headers={'Accept': 'application/json', 'Content-Type': 'application/json'},  auth=('admin', 'admin'))
            
        if response:
                body = response.json()
                return body
            
        return None
    


    def len_ais(self):
        my_brains = self.context.portal_catalog(portal_type=['action_items'], assigned_id=self.get_current())
        
        if my_brains:        
            return len(my_brains)
    
    def count_ais(self):
        urgencies = self.context.portal_catalog.uniqueValuesFor("urgency")
        if urgencies:
            urgency_list = []
            for urgency in reversed(urgencies):
                my_brains = self.context.portal_catalog(portal_type=['action_items'], assigned_id=self.get_current(), urgency=urgency)
                
                urgency_list.append({'name': urgency, 'count': len(my_brains)})
            return urgency_list
            
        return None


    def len_meetings(self):
        # urgencies = self.context.portal_catalog.uniqueValuesFor("meeting_types")
        my_brains = self.context.portal_catalog(portal_type=['meeting', 'Meeting'], attendees=self.get_current()  )
        return len(my_brains)
        # return None
        
    def count_meetings(self):
        meeting_types = self.context.portal_catalog.uniqueValuesFor("meeting_type")
        if meeting_types:
            meeting_list = []
            for meeting_type in meeting_types:
                my_brains = self.context.portal_catalog(portal_type=['meeting', 'Meeting'], attendees=self.get_current(), meeting_type=meeting_type)
                meeting_list.append({'name': meeting_type, 'count': len(my_brains)})
            return meeting_list
            
        return None