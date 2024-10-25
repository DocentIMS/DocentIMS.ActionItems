# -*- coding: utf-8 -*-
from plone import api
from plone.restapi.interfaces import IExpandableElement
from plone.restapi.services import Service
from zope.component import adapter
from zope.interface import Interface
from zope.interface import implementer


@implementer(IExpandableElement)
@adapter(Interface, Interface)
class ItemCount(object):

    def __init__(self, context, request):
        self.context = context.aq_explicit
        self.request = request

    def __call__(self, expand=False):
        # user = None
        # if hasattr(self.request, "user"):
        #     user = self.request.user
        
        result = {
            'item_count': {
                '@id': '{}/@item_count'.format(
                    self.context.absolute_url(),
                ),
            },
        }
        if not expand:
            return result

        # === Your custom code comes here ===
        
        # portal = api.portal.get()
        # current_user = api.user.get_current()
        fullname = "Unknown user"
        current_user =  api.user.get(userid='wglover@docentims.com') 
        if current_user:
            current_user.getProperty("fullname")
        
        #Count meetings
        query = {}
        query['portal_type'] = "meeting"
        #query['something'] = Find my meeetings, might have to search on group
        #Total number of Meetings
        queryresult =  api.content.find(**query)
        all_meetings = len(queryresult)
        
        meeting_types = self.context.portal_catalog.uniqueValuesFor("meeting_type")
        # Meeting list will show count of diffrent meeting types
        meeting_list = []
        if meeting_types:
            for meeting_type in meeting_types:
                my_brains = self.context.portal_catalog(portal_type=['meeting', 'Meeting'], meeting_type=meeting_type)
                meeting_list.append({'name': meeting_type, 'count': len(my_brains)})
            
        query = {}
        query['portal_type'] = "action_items"
        queryresult =  api.content.find(**query)
        all_ais = len(queryresult)
        
        
        urgency_list = []
        urgencies = self.context.portal_catalog.uniqueValuesFor("urgency")
        if urgencies:
            for urgency in reversed(urgencies):
                my_brains = self.context.portal_catalog(portal_type=['action_items'], urgency=urgency)
                
                # list of all action items 'sorted on urgency'
                urgency_list.append({'name': urgency, 'count': len(my_brains)})
            
        
        meetings_and_ais = { 'meetings': all_meetings, 'meeting_list': meeting_list, 'ais': all_ais, 'urgency_list': urgency_list, 'user':  fullname}
        # current_user.getProperty("fullname"
        
        result['item_count']['dashboard-list'] =  meetings_and_ais
        return result


class ItemCountGet(Service):

    def reply(self):
        service_factory = ItemCount(self.context, self.request)
        return service_factory(expand=True)['item_count']
