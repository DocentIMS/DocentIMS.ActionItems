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
        user = None
        
        
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
        if hasattr(self.request, "user"):
            user = self.request.user
        
        fullname = "Unknown user"
        current_user =  api.user.get(userid=user) 
        if current_user:
            user_id = current_user.getProperty("id")
            fullname = current_user.getProperty("fullname")
            
            #Count notificatons
            query = {}
            query['portal_type'] = "Notification"
            query['message_assigned'] = user_id
            queryresult =  api.content.find(**query)
            notifications = len(queryresult)
        
            #Count meetings
            query = {}
            query['portal_type'] = "meeting"
            query['attendees'] = user_id
            #query['something'] = Find my meeetings, might have to search on group
            #Total number of Meetings
            queryresult =  api.content.find(**query)
            all_meetings = len(queryresult)
            
            meeting_types = self.context.portal_catalog.uniqueValuesFor("meeting_type")
            # Meeting list will show count of diffrent meeting types
            meeting_list = []
            if meeting_types:
                for meeting_type in meeting_types:
                    my_brains = self.context.portal_catalog(portal_type=['meeting', 'Meeting'], attendees= user_id, meeting_type=meeting_type)
                    meeting_list.append({'name': meeting_type, 'count': len(my_brains)})
                
            query = {}
            query['portal_type'] = "action_items"
            query['assigned_id'] = user_id
            queryresult =  api.content.find(**query)
            all_ais = len(queryresult)
            
            
            urgency_list = []
            urgencies = self.context.portal_catalog.uniqueValuesFor("urgency")
            if urgencies:
                for urgency in reversed(urgencies):
                    my_brains = self.context.portal_catalog(portal_type=['action_items'], urgency=urgency, assigned_to = user_id)
                    
                    # list of all action items 'sorted on urgency'
                    urgency_list.append({'name': urgency, 'count': len(my_brains)})
                
            
            meetings_and_ais = { 
                                'site_url': self.context.absolute_url(), 
                                'meetings': all_meetings, 
                                'meeting_list': meeting_list, 
                                'ais': all_ais, 
                                'notifications': notifications, 
                                'urgency_list': urgency_list, 
                                'project_color': api.portal.get_registry_record('DocentIMS.ActionItems.interfaces.IDocentimsSettings.color1'),
                                'short_name': api.portal.get_registry_record('DocentIMS.ActionItems.interfaces.IDocentimsSettings.project_short_name'),                                        
                                'user': fullname }
            
            # current_user.getProperty("fullname"
            
            result['item_count']['dashboard-list'] =  meetings_and_ais
            return result
        
        result['item_count']['dashboard-list'] = None
        return result


class ItemCountGet(Service):

    def reply(self):
        service_factory = ItemCount(self.context, self.request)
        return service_factory(expand=True)['item_count']
