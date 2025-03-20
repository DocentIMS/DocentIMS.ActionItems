# -*- coding: utf-8 -*-

from plone.app.layout.viewlets import ViewletBase
from plone import api


class ToolBarViewlet(ViewletBase):

    def update(self):
        self.message = self.get_message()

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
    
    # def red_count(self): 
    #     user_ids = self.current_user.getId()
    #     return self.context.portal_catalog.unrestrictedSearchResults(portal_type=['action_items'], urgency="Red", assigned_to = user_ids)
                     
    
    def index(self):
        return super(ToolBarViewlet, self).render()
    

