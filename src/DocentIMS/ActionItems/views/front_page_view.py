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
        last_login = current.getProperty('last_login_time')
        #fullname = current.getProperty('fullname')
        #melding = "Welcome"
        #if fullname:
        #    melding = "Welcome back {}!".format(fullname)
        if last_login and last_login.year() == 2000:
            fullname = current.getProperty('fullname')
            melding = "Welcome {}!".format(fullname)
            
            api.portal.show_message(
                        message=melding,
                        request=self.request,
                        type="message",
                    )
        return self.index()

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
            