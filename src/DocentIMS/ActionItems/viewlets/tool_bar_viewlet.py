# -*- coding: utf-8 -*-

from plone.app.layout.viewlets import ViewletBase
from plone import api
from DocentIMS.ActionItems.interfaces import IDocentimsSettings
import requests


class ToolBarViewlet(ViewletBase):

    def update(self):
        self.message = self.get_message()
        
    # def basik(self):
    #     return  api.portal.get_registry_record('dashboard', interface=IDocentimsSettings) or ''

    def get_message(self):
        return u'My message'
    
    def tasks_red(self):
        user_ids = self.current_user_id()
        items =  api.content.find( stoplight="Red", assigned_id = user_ids, limit=9, )
        return len(items)
    
    def tasks_green(self):
        user_ids = self.current_user_id()
        items =  api.content.find( stoplight="Green", assigned_id = user_ids, limit=9,
        )
        return len(items)
    
    def tasks_yellow(self):
        user_ids = self.current_user_id()
        items =  api.content.find( stoplight="Yellow", assigned_id = user_ids, limit=9,)
        return len(items)

    def notifications_red(self):
        user_ids = self.current_user_id()
        items =  api.content.find( notification_type="error", notification_assigned = user_ids, limit=9,) 
        return len(items)
 
    
    def notifications_green(self):
        user_ids = self.current_user_id()
        items =  api.content.find( notification_type="info", notification_assigned = user_ids, limit=9,) 
        return len(items)
    
    def notifications_yellow(self):
        user_ids = self.current_user_id()
        items =  api.content.find( notification_type="warning", notification_assigned = user_ids, limit=9,) 
        return len(items)
    
    def color(self):
        return api.portal.get_registry_record('DocentIMS.ActionItems.interfaces.IDocentimsSettings.color1')
 
    def project_name(self):
        return api.portal.get_registry_record('DocentIMS.ActionItems.interfaces.IDocentimsSettings.project_short_name')     
    
    def portal_url(self):
        return  api.portal.get().absolute_url()   
    
    def current_user_id(self):
        current_user =  api.user.get_current()
        return current_user.getId()
    
    def get_sites(self):
        usermail = self.current_user_id()
        basik = api.portal.get_registry_record('dashboard', interface=IDocentimsSettings) or ''
        siteurl = f'https://dashboard.docentims.com/@dashboard_sites/?email={usermail}'
        buttons = []
        try:                
            response  = requests.get(
                siteurl,
                headers={
                    'Accept': 'application/json',
                    'Content-Type': 'application/json',
                },
                auth=('admin', 'admin')                      
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
    

