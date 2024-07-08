# -*- coding: utf-8 -*-
from plone import api
from plone.restapi.interfaces import IExpandableElement
from plone.restapi.services import Service
from zope.component import adapter
from zope.interface import Interface
from zope.interface import implementer
from zExceptions import BadRequest

from zope.component import getUtility
from zope.component import getUtilitiesFor
from plone.dexterity.interfaces import IDexterityFTI
from Products.CMFCore.utils import getToolByName
import json

def get_content_types_and_workflows():
    portal = api.portal.get()
    workflow_tool = getToolByName(portal, 'portal_workflow')
    content_types = getUtilitiesFor(IDexterityFTI)

    result = []

    for name, fti in content_types:
        workflows = workflow_tool.getWorkflowsFor(fti.factory)
        if workflows:
            workflow = workflows[0]  # Assuming one workflow per content type
            states = list(workflow.states)
            result.append({
                'content_type': name,
                'workflow_states': states
            })

    return result
    #return json.dumps(result, indent=2)



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
        portal = api.portal.get()
    
        companies = api.portal.get_registry_record('DocentIMS.ActionItems.interfaces.IDocentimsSettings.companies')
        download_date = ''
        downloads_folder = portal.get('downloads', False)
        team_member_folder =  downloads_folder.get('team_member', False)
        
        if  team_member_folder:
            download_date = team_member_folder.modified().strftime("%m/%d/%Y, %H:%M:%S")
        
        if user is not None:    
            result = {
                'docs_info': {
                    'project_color': api.portal.get_registry_record('DocentIMS.ActionItems.interfaces.IDocentimsSettings.color1'),
                    'very_short_name': api.portal.get_registry_record('DocentIMS.ActionItems.interfaces.IDocentimsSettings.very_short_name', None),
                    'short_name': api.portal.get_registry_record('DocentIMS.ActionItems.interfaces.IDocentimsSettings.project_short_name'),
                    'project_contract_number':   api.portal.get_registry_record('DocentIMS.ActionItems.interfaces.IDocentimsSettings.project_contract_number'),   
                    'project_document_naming_convention':   api.portal.get_registry_record('DocentIMS.ActionItems.interfaces.IDocentimsSettings.project_document_naming_convention'),
                    'companies' :  companies,
                    'last_document_save_locations' : download_date,  
                    'wf_states_list' : get_content_types_and_workflows(),

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
