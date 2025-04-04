# -*- coding: utf-8 -*-
from plone import api
from plone.restapi.interfaces import IExpandableElement
from plone.restapi.services import Service
from zope.component import adapter
from zope.interface import Interface
from zope.interface import implementer
from Products.CMFCore.utils import getToolByName
from zope.component import getUtility
from zope.component import getUtilitiesFor
from plone.dexterity.interfaces import IDexterityFTI

import json

# curl -i -X GET https://mymeadows.org/@workflow_info?portal_type=* -H "Accept: application/json" -k --user user:password


def get_content_types_and_workflows(portal_type):
    # portal_types = request.portal_type or None
    
    portal = api.portal.get()
    types = api.portal.get_tool('portal_types')
    workflow_tool = getToolByName(portal, 'portal_workflow')
    # wft = api.portal.get_tool('portal_workflow')
    # content_types = getUtilitiesFor(IDexterityFTI)
    content_types =  types.listContentTypes()

    result = []
    
    
    

    # for name, fti in content_types:
    for c_type in content_types:
        if c_type == portal_type or c_type.lower() == portal_type or c_type.lower().replace(" ", "_") == portal_type or portal_type == "*":
        
            workflows = workflow_tool.getWorkflowsFor(c_type)
            if workflows:
                workflow = workflows[0]  
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
                    'content_type': c_type,
                    'workflow_transitions': transitions,
                    'workflow_states': states,
                    'initial_state' :  workflow.initial_state,
                })

    return result
     





@implementer(IExpandableElement)
@adapter(Interface, Interface)
class WorkflowInfo(object):

    def __init__(self, context, request):
        self.context = context.aq_explicit
        self.request = request

    def __call__(self, expand=False):
        # if not expand:
        #     return result
        
        portal_type = None
        if hasattr(self.request, "portal_type"):
            portal_type = self.request.portal_type
            
            
            
            return {
                    'workflow_info': {
                    'wf_states_list' : get_content_types_and_workflows(portal_type=portal_type),
                    },
            }
        
        return  {
            'workflow_info': {
                '@id': '{}/workflow_info'.format(
                    self.context.absolute_url(),
                ),
            },
        }


class WorkflowInfoGet(Service):

    def reply(self):
        service_factory = WorkflowInfo(self.context, self.request)
        return service_factory(expand=True)['workflow_info']
