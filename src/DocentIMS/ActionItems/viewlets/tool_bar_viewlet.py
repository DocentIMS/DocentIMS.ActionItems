# -*- coding: utf-8 -*-

from plone.app.layout.viewlets import ViewletBase
from plone import api
from DocentIMS.ActionItems.interfaces import IDocentimsSettings
import requests
from plone.memoize.view import memoize
from plone.memoize import ram
import time
from zope.component import getUtility
from plone.registry.interfaces import IRegistry

from urllib.parse import urlparse


# def sites_cache_key(method, self):
#     usermail = self.current_user_id()
#     if not usermail:
#         return None  # Don't cache if no user

#     # Cache key changes every 10 minutes (600 seconds)
#     time_bucket = int(time.time() / 600)
#     return (usermail, time_bucket)

class ToolBarViewlet(ViewletBase):
    
    def sites_cache_key(method, self):
        usermail = self.current_user_id
        if not usermail:
            return None  # Don't cache if no user

        # Cache key changes every 100 minutes (6000 seconds)
        time_bucket = int(time.time() / 6000)
        return (usermail, time_bucket)
    
    def is_project_manager(self):
        current_user =  api.user.get_current()
        return "PrjMgr" in current_user.getGroups()
        
    def basik(self):
         return  api.portal.get_registry_record('dashboard', interface=IDocentimsSettings) or ''

    def tasks_red(self):
        user_ids = self.current_user_id
        stoplight_state = self.stoplight_state  
        items =  api.content.find(stoplight="Red", assigned_id = user_ids, review_state=stoplight_state, limit=9)
        return len(items)
    
    def tasks_green(self):
        user_ids = self.current_user_id
        stoplight_state = self.stoplight_state
        items =  api.content.find(stoplight="Green", assigned_id = user_ids, review_state=stoplight_state, limit=9)
        return len(items)
    
    def tasks_yellow(self):
        user_ids = self.current_user_id
        stoplight_state = self.stoplight_state
        items =  api.content.find(stoplight="Yellow", assigned_id = user_ids, review_state=stoplight_state, limit=9)
        return len(items)

    def notifications_red(self):
        user_ids = self.current_user_id
        items =  api.content.find( notification_type="error", notification_assigned = user_ids, limit=9,) 
        return len(items)
 
    def notifications_green(self):
        user_ids = self.current_user_id
        items =  api.content.find( notification_type="info", notification_assigned = user_ids, limit=9,) 
        return len(items)
    
    def notifications_yellow(self):
        user_ids = self.current_user_id
        items =  api.content.find( notification_type="warning", notification_assigned = user_ids, limit=9,) 
        return len(items)

    @memoize
    def get_the_tooltips(self):
        registry = getUtility(IRegistry)
        
        # TO Do: Why does this not return all
        #settings = registry.forInterface(IDocentimsSettings, check=False)        
        # works
        #api.portal.get_registry_record('DocentIMS.ActionItems.interfaces.IDocentimsSettings.tooltipIdButtonAbout')
        
        prefix = 'DocentIMS.ActionItems.interfaces.IDocentimsSettings.'
        
        tooltip_values = {
                key.replace(prefix, ''): registry.records[key].value
                for key in registry.records.keys()
                if key.startswith(prefix + 'tooltip')
        }
                
        return tooltip_values
    
    
    @property
    def color(self):
        return api.portal.get_registry_record('DocentIMS.ActionItems.interfaces.IDocentimsSettings.color1')
    
    @property
    def stoplight_state(self):
        return api.portal.get_registry_record('DocentIMS.ActionItems.interfaces.IDocentimsSettings.stoplight_state')
    
    @property
    def project_name(self):
        return api.portal.get_registry_record('DocentIMS.ActionItems.interfaces.IDocentimsSettings.project_short_name')     
    
    @property
    @memoize
    def portal_url(self):
        return  api.portal.get().absolute_url()   
    
    @property
    @memoize
    def current_user_id(self):
        current_user =  api.user.get_current()
        return current_user.getId()

    @ram.cache(sites_cache_key)
    def get_sites(self):
        import pdb; pdb.set_trace()
        user = api.user.get_current()
        usermail = user.getProperty('email')
        if usermail:
            basik = api.portal.get_registry_record('dashboard', interface=IDocentimsSettings) or ''
            if basik:
                siteurl = f'https://dashboard.docentims.com/@dashboard_sites/?email={usermail}'
                buttons = []
                try:                
                    response  = requests.get(
                        siteurl,
                        headers={
                            'Accept': 'application/json',
                            'Content-Type': 'application/json',
                            'Authorization': f'Basic {basik}',
                        },
                        timeout=2,                    
                    )

                    if response.status_code == 200:
                        #body = response.json()                    
                        return response.json()

                        
                except requests.exceptions.ConnectionError:
                    print("Failed to connect to the server. Please check your network or URL.")
                except requests.exceptions.Timeout:
                    print("The request timed out. Try again later.")
                except requests.exceptions.RequestException as e:
                    print(f"An error occurred: {e}")
            
        return None
    
    # def red_count(self): 
    #     user_ids = self.current_user.getId()
    #     return self.context.portal_catalog.unrestrictedSearchResults(portal_type=['action_items'], urgency="Red", assigned_to = user_ids)
                     
    
    def index(self):
        return super(ToolBarViewlet, self).render()
    
    def webmail_url(self):
        site_url = self.portal_url
        parsed_url = urlparse(site_url)
        hostname = parsed_url.hostname  # "test.myurl.com"

        # Get the domain part (strip subdomains)
        domain_parts = hostname.split('.')
        if len(domain_parts) >= 2:
            domain = '.'.join(domain_parts[-2:])  # e.g., "myurl.com"
        else:
            domain = hostname  # fallback

        return domain

    

