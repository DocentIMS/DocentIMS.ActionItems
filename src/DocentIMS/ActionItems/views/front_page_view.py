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
        # Implement your own actions:
        current = api.user.get_current()
        #import pdb; pdb.set_trace()
        last_login = current.getProperty('last_login_time')
        if last_login and last_login.year() == 2000:
            fullname = current.getProperty('fullname')
            melding = "Welcome {}!".format(fullname)
            
            api.portal.show_message(
                        message=melding,
                        request=self.request,
                        type="message",
                    )
        return self.index()
    
    def field_to_return(self):
        current = api.user.get_current()
        
        
        if current and current.getUserName() != 'Anonymous User':
            #last_login = current.getProperty('last_login_time') or None
            #import pdb; pdb.set_trace()
            year = 2023
            last_login =   current.getProperty('last_login_time') 
            if last_login:
                year = last_login.year()
            
            group = api.group.get(groupname='PrjTeam')
            pr_man_group = api.group.get(groupname='PrjMgr')
            roles =  api.user.get_roles(user=current)
            
            #first login
            #import pdb; pdb.set_trace()
            if year < 2024:
                
                #import pdb; pdb.set_trace()
        
            
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
            
            if  year >= 2023:
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
            