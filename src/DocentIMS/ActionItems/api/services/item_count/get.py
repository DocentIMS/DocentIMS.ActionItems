# -*- coding: utf-8 -*-
from plone import api
from plone.restapi.interfaces import IExpandableElement
from plone.restapi.services import Service
from zope.component import adapter
from zope.interface import Interface
from zope.interface import implementer
from DateTime import DateTime
import datetime

from DocentIMS.ActionItems.interfaces import IDocentimsSettings


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
        your_team_role = ""
        current_user =  api.user.get(userid=user) or api.user.get(username=user) 
        if current_user:
            user_ids = [current_user.getUserName(), current_user.getUserId(), current_user.getProperty("email") ] 
            fullname = current_user.getProperty("fullname", None)
            your_team_role = current_user.getProperty("your_team_role", None)
            
            
            #Count notificatons
            notification_list = []
            notification_types = ["error", "warning",  "info"]
            for notification_type in notification_types:
                    my_brains = self.context.portal_catalog(portal_type=['Notification'], 
                                                                message_assigned = user_ids, 
                                                                notification_type=notification_type)
                    notification_list.append({'name': notification_type, 'count': len(my_brains)})
        
        
            #Count meetings
            query = {}
            query['portal_type'] = "meeting"
            query['attendees'] = user_ids
            #query['something'] = Find my meeetings, might have to search on group
            #Total number of Meetings
            queryresult =  api.content.find(**query)
            all_meetings = len(queryresult)
            
            #meeting_types = self.context.portal_catalog.uniqueValuesFor("meeting_type")
            meeting_types =  api.portal.get_registry_record('DocentIMS.ActionItems.interfaces.IDocentimsSettings.meeting_types')
            
            # Meeting list will show count of diffrent meeting types
            meeting_list = []
            if meeting_types:
                for meeting_type in meeting_types:
                    mtype= meeting_type['meeting_type']
                    my_brains = self.context.portal_catalog(
                        portal_type=['meeting', 'Meeting'], 
                        attendees= user_ids, 
                        meeting_type=mtype)
                    meeting_list.append({'name': mtype, 'count': len(my_brains)}) 
        
                
            query = {}
            query['portal_type'] = "action_items"
            query['assigned_id'] = user_ids
            queryresult =  api.content.find(**query)
            all_ais = len(queryresult)
            
            
            urgency_list = []
            #urgencies = self.context.portal_catalog.uniqueValuesFor("urgency")
            
            red = api.portal.get_registry_record('urgent_red', interface=IDocentimsSettings)
            yellow = api.portal.get_registry_record('soon_yellow', interface=IDocentimsSettings)
            green = api.portal.get_registry_record('future_green', interface=IDocentimsSettings)
        
            urgencies = ["Urgent < {days} workdays".format(days = red),
                         "Soon < {days} workdays".format(days = yellow),
                         "Future < {days} workdays".format(days = green),
                         "More than {days}".format(days = green),
                         "Unset",
                        ]

            
            for urgency in  urgencies:
                    my_brains = self.context.portal_catalog(portal_type=['action_items'], urgency=urgency, assigned_to = user_ids)
                    
                    # list of all action items 'sorted on urgency'
                    urgency_list.append({'name': urgency, 'count': len(my_brains)})
                
            
            

            # Query the catalog for items, sorted by ModificationDate in descending order
            # There will always be a catalog entry, no need to check
            last_item = self.context.portal_catalog(
                        sort_on='modified',
                        sort_order='descending',
                        sort_limit=1,
                )     
            
            last_date = last_item[0].modified
            human_readable_date = last_date.strftime('%A, %d %B %Y, %I:%M %p')
            
            meetings_and_ais = { 
                                'site_url': self.context.absolute_url(), 
                                'meetings': all_meetings, 
                                'meeting_list': meeting_list, 
                                'last_updated': human_readable_date,
                                # 'human_readable_date': human_readable_date,
                                # 'last_modified': last_modified,
                                # 'last_updated':  datetime.datetime.strptime(str(last_modified), '%Y-%m-%dT%H:%M:%S').strftime('%A, %d %B %Y, %I:%M %p'),    
                                'ais': all_ais, 
                                'your_team_role': your_team_role,
                                'notification_list': notification_list, 
                                'urgency_list': urgency_list, 
                                'project_color': api.portal.get_registry_record('DocentIMS.ActionItems.interfaces.IDocentimsSettings.color1'),
                                'mark_color': api.portal.get_registry_record('DocentIMS.ActionItems.interfaces.IDocentimsSettings.color2'),
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
