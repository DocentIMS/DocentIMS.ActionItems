# -*- coding: utf-8 -*-

# from DocentIMS.ActionItems import _
from Products.Five.browser import BrowserView
from zope.interface import Interface

from plone import api

# from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile


class ITeamView(Interface):
    """ Marker Interface for ITeamView"""


class TeamView(BrowserView):
    # If you want to define a template here, please remove the template from
    # the configure.zcml registration of this view.
    # template = ViewPageTemplateFile('team_view.pt')

    def __call__(self):
        # Implement your own actions:
        return self.index()
    
    def get_group_members(self):
        group_id = "PrjTeam"
        users = api.group.get(group=group_id).getMembers()
        # userlist = []
        
        return [{'name': user.getProperty('fullname') or user.getId(), 'role': user.getProperty('your_team_role'), 'company': user.getProperty('company'), } for user in users]



