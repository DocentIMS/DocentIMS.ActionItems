# -*- coding: utf-8 -*-
from plone import api
from plone.restapi.interfaces import IExpandableElement
from plone.restapi.services import Service
from zope.component import adapter
from zope.interface import Interface
from zope.interface import implementer
from zExceptions import BadRequest


@implementer(IExpandableElement)
@adapter(Interface, Interface)
class MyEmail(object):

    def __init__(self, context, request):
        self.context = context.aq_explicit
        self.request = request

    def __call__(self, expand=False):
        result = {
            'my_email': {
                '@id': '{}/@my_email'.format(
                    self.context.absolute_url(),
                ),
            },
        }
        if not expand:
            return result

        # === Your custom code comes here ===

        user = api.user.get_current()   
        # We are not using the option to get another user
        # usermail = self.request.get('email', None)
        # Only users with special permissions can get info about other users
        # if usermail and usermail is not None and 'User Api' in api.user.get_roles(user.id):
        # user = api.user.get(username=usermail) 
        
        # companies = api.portal.get_registry_record('DocentIMS.ActionItems.interfaces.IDocentimsSettings.companies')
        if user.name != 'Anonymous User' and  user is not None: 
            my_groups = user.getGroups() or None
            # Get all, something like this:
            # my_groups = api.group.get_groups()
            # need to serilize below
            # and use id, not name
            # group_names = [group.id for group in all_groups]
            # Then a check if my_group is empty (did not need that check with own group because at least 'I' am part of it)
            
            members = []
            if my_groups:   
               
                for mygroup in my_groups:
                    ids = []
                    groupmembers = api.user.get_users(groupname=mygroup)
                    for groupmember in groupmembers:
                        ids.append({
                            'id': groupmember.getId(), 
                            'fullname': groupmember.getProperty('fullname'), 
                            'email': groupmember.getProperty('email')
                        })
                        
                    
                    members.append({'id': mygroup.getId(), 'id': mygroup.getGroupName(), 'members': ids})
                    # print(members)
                members=members
                 
            result = {
                'my_email': {
                    'id': user.getProperty('id'),
                    'email': user.getProperty('email'),
                    'fullname' : user.getProperty('fullname'),   
                    # 'old_groups': my_groups,
                    'groups': members,
                    'roles' : user.getRoles(),
                    'last_name' : user.getProperty('fullname'), 
                    'first_name' : user.getProperty('first_name'), 
                    'your_team_role': user.getProperty('your_team_role'), 
                    'office_phone_number': user.getProperty('office_phone_number'), 
                    'cellphone_number': user.getProperty('cellphone_number'), 
                    'company' : user.getProperty('company'), 
                    'planning_project': api.portal.get_registry_record('DocentIMS.ActionItems.interfaces.IDocentimsSettings.planning_project'),
                    
                },
            }
            
        
            return result
        
        #raise BadRequest("Parameters supplied are not valid")
        result = {
                'my_email': {
                    'id': None,
                },
            }
        return result
        #self.request.response.setStatus(401)


class MyEmailGet(Service):

    def reply(self):
        service_factory = MyEmail(self.context, self.request)
        return service_factory(expand=True)['my_email']
