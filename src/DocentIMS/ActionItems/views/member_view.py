# -*- coding: utf-8 -*-

# from DocentIMS.ActionItems import _
from Products.Five.browser import BrowserView
from zope.interface import Interface
from plone.dexterity.utils import iterSchemata
from zope.schema import getFields
from plone import api
from urllib.parse import urlparse


# ## -*- coding: utf-8 -*-
# from zope.interface import  Interface

# from Products.Five import BrowserView
 
# 

# from Products.CMFCore.utils import getToolByName
 
 

# import logging

# logger = logging.getLogger(__file__)

# from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile


class IMemberView(Interface):
    """ Marker Interface for IMemberView"""


class MemberView(BrowserView):
    # If you want to define a template here, please remove the template from
    # the configure.zcml registration of this view.
    # template = ViewPageTemplateFile('member_view.pt')

    def __call__(self):
        # Implement your own actions:
        return self.index()

    # def all_users(self):
    #     return api.user.get_users()
    
    
    def get_webmail_url(self):
        portal_url =  api.portal.get().absolute_url()   
        parsed_url = urlparse(portal_url)
        hostname = parsed_url.hostname  # "test.myurl.com"

        # Get the domain part (strip subdomains)
        domain_parts = hostname.split('.')
        if len(domain_parts) >= 2:
            domain = '.'.join(domain_parts[-2:])  # e.g., "myurl.com"
        else:
            domain = hostname  # fallback

        return domain

    @property
    def group_users(self):
        userlist = []
        for member in api.user.get_users():
            userlist.append(
                { 'id': member.getProperty('id'), 
                'email': member.getProperty('email'),
                'fullname': member.getProperty('fullname'),
                'last_name': member.getProperty('last_name'),
                'first_name': member.getProperty('first_name'),
                'your_team_role': member.getProperty('your_team_role'),
                'office_phone_number': member.getProperty('office_phone_number'),
                'cellphone_number': member.getProperty('cellphone_number'),
                'company': member.getProperty('company'),
                'returning': member.getProperty('returning'),
                'login_time': member.getProperty('login_time'),
                'verified': (member.getProperty('login_time').strftime('%Y') == '2000'),
                 })

        return sorted(userlist, key=lambda medlem: medlem['last_name'])
        #return userlist

 
 

