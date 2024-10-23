# -*- coding: utf-8 -*-

from plone.app.event.browser.event_summary import EventSummaryView

# from DocentIMS.ActionItems import _
from plone import api
# from plone.protect.interfaces import IDisableCSRFProtection



class MeetingSummaryView(EventSummaryView):
    
    @property
    def get_attendees(self):
        # alsoProvides(self.request, IDisableCSRFProtection)
        attendees = list(self.data.attendees)
        attendees_groups = self.context.attendees_group
        if  attendees_groups:
            for meeting_group in attendees_groups:
                groupmembers = api.user.get_users(groupname=meeting_group)
                for groupmember in groupmembers:
                    attendees.append(groupmember.getId())
            attendees = set(attendees)
            
            # self.data.attendees = attendees        
        return tuple(attendees)
    
    

    
 
    