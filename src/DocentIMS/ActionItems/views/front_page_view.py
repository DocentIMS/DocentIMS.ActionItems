 
        
            
            
# -*- coding: utf-8 -*-

# from DocentIMS.ActionItems import _
from Products.Five.browser import BrowserView
from zope.interface import Interface
from plone import api
from datetime import datetime
import DateTime
from DocentIMS.ActionItems.interfaces import IDocentimsSettings

# from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile


class IFrontPageView(Interface):
    """ Marker Interface for IFrontPageView"""


class FrontPageView(BrowserView):
    # If you want to define a template here, please remove the template from
    # the configure.zcml registration of this view.
    # template = ViewPageTemplateFile('front_page_view.pt')

    def __call__(self):
        
        return self.index()
    
    def field_to_return(self):
        
        
        #if current and  not current.isAnonymousUser():
        #if current and current.getUserName() != 'Anonymous User':
        if not api.user.is_anonymous():
            current = api.user.get_current()
            #last_login =   current.getProperty('last_login_time')
            returning_user =  current.getProperty('returning', False)
            current.setProperties(returning = True)
            group = api.group.get(groupname='PrjTeam')
            pr_man_group = api.group.get(groupname='PrjMgr')
            roles =  api.user.get_roles(user=current)
            
            if not returning_user:
                
                if 'Project Manager' in roles:
                    #User is project manager
                    return self.context.first_login_prjmgr
                
                if current.getUserId() in pr_man_group.getAllGroupMemberIds():
                    #User is project manager group
                    return self.context.first_login_prjmgr
                
                #Check if user is part of PrjTEam group
                if current.getUserId() in group.getAllGroupMemberIds():
                    #User is team
                    return self.context.first_login_teammbr
            
            return self.context.frontpage_text
            
        return self.context.frontpage_anon
    
    
        

    def last_login(self):
        current = api.user.get_current()
        last_login = current.getProperty('last_login_time')
        if last_login.year() == 2000:
            return 'Welcome, new user, this is your first login'
            
        return 'Welcome back'
    
    @property
    def project_title(self):
        return api.portal.get_registry_record('project_title', interface=IDocentimsSettings)
            
    @property
    def project_short_name(self):
        return api.portal.get_registry_record('project_short_name', interface=IDocentimsSettings)     
        
    @property
    def project_description(self):
        return api.portal.get_registry_record('project_description', interface=IDocentimsSettings)
            