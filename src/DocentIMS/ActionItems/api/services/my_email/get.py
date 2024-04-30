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
            
        if user is not None:    
            result = {
                'my_email': {
                    'id': user.getProperty('id'),
                    'email': user.getProperty('email'),
                    'fullname' : user.getProperty('fullname'),   
                    'groups': user.getGroups(),
                    'roles' : user.getRoles(),
                    'last_name' : user.getProperty('fullname'), 
                    'first_name' : user.getProperty('first_name'), 
                    'your_team_role': user.getProperty('your_team_role'), 
                    'office_phone_number': user.getProperty('office_phone_number'), 
                    'cellphone_number': user.getProperty('cellphone_number'), 
                    'company' : user.getProperty('company'), 
                    'project_color': api.portal.get_registry_record('DocentIMS.ActionItems.interfaces.IDocentimsSettings.color1'),
                    'very_short_name':  api.portal.get_registry_record('DocentIMS.ActionItems.interfaces.IDocentimsSettings.very_short_name'),
                    'short_name':       api.portal.get_registry_record('DocentIMS.ActionItems.interfaces.IDocentimsSettings.project_short_name'),
                    'project_contract_number':   api.portal.get_registry_record('DocentIMS.ActionItems.interfaces.IDocentimsSettings.project_contract_number')         
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
