# -*- coding: utf-8 -*-
from plone import api
from plone.restapi.interfaces import IExpandableElement
from plone.restapi.services import Service
from zope.component import adapter
from zope.interface import Interface
from zope.interface import implementer
from zExceptions import BadRequest
from datetime import datetime
from pytz import timezone

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
            #states = list(workflow.states)
            # transitions = list(workflow.transitions) 
            transitions = []
            states = []
            for transition_id, transition in workflow.transitions.items():
                transitions.append({ 
                    'id': transition_id, 
                    'title': transition.title or transition_id,
                    'description': transition.description,
                    'new_state_id': transition.new_state_id,
                    'actbox_name': transition.actbox_name,
                    
                })
                 
            for state_id, workflow_state in workflow.states.items():
                states.append({ 
                    'id': state_id, 
                    'title': workflow_state.title or state_id,
                    'description': workflow_state.description,
                    'transitions': workflow_state.transitions    
                })
                 
                
            result.append({
                'content_type': name,
                'workflow_transitions': transitions,
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
        downloads_folder = portal.get('downloads', False)
        team_member_folder =  downloads_folder.get('team_member', False)
        
        portal_timezone = api.portal.get_registry_record('plone.portal_timezone')
        user_timezone = user.getProperty('timezone') or portal_timezone
            
        if  team_member_folder:
            down_load_date = team_member_folder.modified().asdatetime().astimezone(timezone(portal_timezone)).isoformat()
        
        if user is not None:    
            
            # if user.getProperty('timezone')  and user.getProperty('timezone')  != None:
            #     user_timezone = user.getProperty('timezone') 
            
            m_types = api.portal.get_registry_record('DocentIMS.ActionItems.interfaces.IDocentimsSettings.meeting_types')
            # Convert sets to lists
            for item in m_types:
                if isinstance(item.get('meeting_attendees'), set):
                    item['meeting_attendees'] = list(item['meeting_attendees'])
                    
            
            result = {
                'docs_info': {
                    'meeting_locations': api.portal.get_registry_record('DocentIMS.ActionItems.interfaces.IDocentimsSettings.location_names'),
                    'meeting_types':  m_types, 
                    'planning_project': api.portal.get_registry_record('DocentIMS.ActionItems.interfaces.IDocentimsSettings.planning_project'),
                    'green' : api.portal.get_registry_record('DocentIMS.ActionItems.interfaces.IDocentimsSettings.future_green'),
                    'yellow' : api.portal.get_registry_record('DocentIMS.ActionItems.interfaces.IDocentimsSettings.soon_yellow'),
                    'red' : api.portal.get_registry_record('DocentIMS.ActionItems.interfaces.IDocentimsSettings.urgent_red'),
                    'project_color': api.portal.get_registry_record('DocentIMS.ActionItems.interfaces.IDocentimsSettings.color1'),
                    'marking_color': api.portal.get_registry_record('DocentIMS.ActionItems.interfaces.IDocentimsSettings.color2'),
                    'very_short_name': api.portal.get_registry_record('DocentIMS.ActionItems.interfaces.IDocentimsSettings.very_short_name', None),
                    'short_name': api.portal.get_registry_record('DocentIMS.ActionItems.interfaces.IDocentimsSettings.project_short_name'),
                    'project_contract_number':   api.portal.get_registry_record('DocentIMS.ActionItems.interfaces.IDocentimsSettings.project_contract_number'),   
                    'project_document_naming_convention':   api.portal.get_registry_record('DocentIMS.ActionItems.interfaces.IDocentimsSettings.project_document_naming_convention'),
                    'companies' :  companies,
                    'last_document_save_location': down_load_date,
                    'time_now_portal': datetime.now().astimezone(timezone(portal_timezone)).isoformat(),
                    'time_now_user': datetime.now().astimezone(timezone(user_timezone)).isoformat(),
                    'user_timezone': user_timezone,
                    'portal_timezone': portal_timezone, 
                    'planning_project': api.portal.get_registry_record('DocentIMS.ActionItems.interfaces.IDocentimsSettings.planning_project'),
                    # 'time_now_isoformat':  datetime.now().isoformat(),
                    'template_password': api.portal.get_registry_record('DocentIMS.ActionItems.interfaces.IDocentimsSettings.template_password')
                    # 'wf_states_list' : get_content_types_and_workflows(),    
                                 
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
