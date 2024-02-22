# -*- coding: utf-8 -*-

# from DocentIMS.ActionItems import _
from Products.Five.browser import BrowserView
from zope.interface import Interface
from plone import api
from datetime import datetime
import DateTime

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
        fullname = current.getProperty('fullname')
        melding = "Welcome back {}!".format(fullname)
        if last_login.year() == 2000:
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
            return 'Welcome, new user'
            
        return 'Welcome back'
