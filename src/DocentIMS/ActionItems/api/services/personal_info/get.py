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
class DocsInfo(object):

    def __init__(self, context, request):
        self.context = context.aq_explicit
        self.request = request

    def __call__(self, expand=False):
        result = {
            'docs_info': {
                '@id': '{}/@docs_info'.format(
                    self.context.absolute_url(),
                ),
            },
        }
        if not expand:
            return result

        # === Your custom code comes here ===

        user = api.user.get_current()   
 
        
        companies = api.portal.get_registry_record('DocentIMS.ActionItems.interfaces.IDocentimsSettings.companies')
              
            
        if user is not None:    
            result = {
                'docs_info': {
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
                    'marking_color': api.portal.get_registry_record('DocentIMS.ActionItems.interfaces.IDocentimsSettings.color2'),
                    'project_color': api.portal.get_registry_record('DocentIMS.ActionItems.interfaces.IDocentimsSettings.color1'),
                    'very_short_name': api.portal.get_registry_record('DocentIMS.ActionItems.interfaces.IDocentimsSettings.very_short_name'),
                    'short_name': api.portal.get_registry_record('DocentIMS.ActionItems.interfaces.IDocentimsSettings.project_short_name'),
                    'project_contract_number':   api.portal.get_registry_record('DocentIMS.ActionItems.interfaces.IDocentimsSettings.project_contract_number'),   
                    'project_document_naming_convention':   api.portal.get_registry_record('DocentIMS.ActionItems.interfaces.IDocentimsSettings.project_document_naming_convention'),
                    'companies' :  companies,
                    'planning_project': api.portal.get_registry_record('DocentIMS.ActionItems.interfaces.IDocentimsSettings.planning_project'),
                    'template_password': api.portal.get_registry_record('DocentIMS.ActionItems.interfaces.IDocentimsSettings.template_password')
                },
            }
            
        
            return result
        
        #raise BadRequest("Parameters supplied are not valid")
        result = {
                'docs_info': {
                    'id': None,
                },
            }
        return result
        #self.request.response.setStatus(401)


class GetDocsInfo(Service):

    def reply(self):
        service_factory = DocsInfo(self.context, self.request)
        return service_factory(expand=True)['docs_info']
