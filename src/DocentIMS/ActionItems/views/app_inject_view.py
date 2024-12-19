# -*- coding: utf-8 -*-

# from DocentIMS.ActionItems import _
from Products.Five.browser import BrowserView
from zope.interface import Interface
import requests
from plone import api

# from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile


class IAppInjectView(Interface):
    """ Marker Interface for IAppInjectView"""


class AppInjectView(BrowserView):
    # If you want to define a template here, please remove the template from
    # the configure.zcml registration of this view.
    # template = ViewPageTemplateFile('app_inject_view.pt')

    # def __init__(self, context, request):
    #     self.request = request
        
        
    def __call__(self):
        # Implement your own actions:
        return self.index()
    
    def get_current(self):
        current = api.user.get_current()
        #return current.getId()
        return current.getProperty('email')
    
    
    def get_dashboard_info(self):
        # import pdb; pdb.set_trace()
        # Change to own api endpoint
        # response = requests.get('http://ubuntu.local:8605/Plone14/@search', headers={'Accept': 'application/json', 'Content-Type': 'application/json'},  auth=('admin', 'admin'))
        siteurl = self.request.get('siteurl', 'https://mymeadows.org')
        
        response = requests.get(f'{siteurl}/@item_count?user={self.get_current()}', headers={'Accept': 'application/json', 'Content-Type': 'application/json'})
            
        if response:
                body = response.json()
                return body
            
        return None
     
     
