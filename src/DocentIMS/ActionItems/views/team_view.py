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
        import pdb; pdb.set_trace()
        grouppe = "Meadows Board"
        groupmembers = api.group.get(groupname=grouppe) 
        userlist = []
        
        for groupmember in groupmembers:
            userlist.append({
                            'id': groupmember.getId(), 
                            'fullname': groupmember.getProperty('fullname'), 
                            'email': groupmember.getProperty('email'),
                            'role': groupmember.getProperty('your_team_role'),
                            'company': groupmember.getProperty('company')
                        })
                        
                
        return userlist
        # return [{'name': user.getProperty('fullname') or user.getId(), 'role': user.getProperty('your_team_role'), 'company': user.getProperty('company'), } for user in users]



