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
        
        current = api.user.get_current()
        users = [api.user.get_current()]
        
        # if api.user.get_current() is not in some group:
            
        # We are not using the option to get another user
        usermail = self.request.get('email', None)
        # Only users with special permissions can get info about other users
        # if usermail and usermail is not None and 'User Api' in api.user.get_roles(user.id):
        # if usermail and usermail is not None and 'User Api' in api.user.get_roles(user.id):
        my_groups = current.getGroups() or None
        import pdb; pdb.set_trace()
        
        if usermail and usermail is not None and usermail != '*':
            users = [api.user.get(username=usermail)] 
            
        elif usermail == '*':
            users = api.user.get_users()
            my_groups =  api.group.get_groups()
        
        # companies = api.portal.get_registry_record('DocentIMS.ActionItems.interfaces.IDocentimsSettings.companies')
        
        members = []
        result = []
        
        
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
                    group = api.group.get(groupname=mygroup)
                    for groupmember in groupmembers:
                        ids.append({
                            'id': groupmember.getId(), 
                            'fullname': groupmember.getProperty('fullname'), 
                            'email': groupmember.getProperty('email')
                        })
                        
                    members.append({'id': group.getId(), 'title': group.getGroupTitleOrName(), 'groupMembers': ids})
                    # print(members)
                members=members
        
        for user in users:
            result.append({
                    'id': user.getProperty('id'),
                    'email': user.getProperty('email'),
                    'fullname' : user.getProperty('fullname'),   
                    # 'groups': members,
                    'roles' : user.getRoles(),
                    'last_name' : user.getProperty('fullname'), 
                    'first_name' : user.getProperty('first_name'), 
                    'your_team_role': user.getProperty('your_team_role'), 
                    'office_phone_number': user.getProperty('office_phone_number'), 
                    'cellphone_number': user.getProperty('cellphone_number'), 
                    'company' : user.getProperty('company'), 
                
            })
        
        
        result.append({'members': members})
        
        return result
        
        


class MyEmailGet(Service):

    def reply(self):
        service_factory = MyEmail(self.context, self.request)
        return service_factory(expand=True) 
        # return service_factory(expand=True)['my_email']
