# -*- coding: utf-8 -*-

from plone.app.event.browser.event_summary import EventSummaryView

# from DocentIMS.ActionItems import _
from plone import api
# from plone.protect.interfaces import IDisableCSRFProtection

class MeetingSummaryView(EventSummaryView):
    
    @property
    def get_attendees(self):
        attendees = list(self.data.attendees)
        attendees_groups = self.context.attendees_group
        if attendees_groups:
            for meeting_group in attendees_groups:
                groupmembers = api.user.get_users(groupname=meeting_group)
                for groupmember in groupmembers:
                    attendees.append(groupmember.getId())
            attendees = set(attendees)
        return tuple(attendees)
    
    @property
    def get_groups(self):
        attendees_groups = self.context.attendees_group
        if attendees_groups:
            groups = []
            for group in attendees_groups:
                group_this = api.group.get(groupname=group)
                groups.append(group_this.getGroupTitleOrName())
            return ", ".join(groups)
        return None

    @property
    def get_groups_with_attendees(self):
        """
        Returns a dictionary:
        {
            'Team A': [user_id1, user_id2],
            'Team B': [user_id3],
        }
        """
        attendees = set(self.get_attendees)
        groups_with_attendees = {}

        for groupname in self.context.attendees_group or []:
            group = api.group.get(groupname=groupname)
            if not group:
                continue
            group_title = group.getGroupTitleOrName()
            group_members = [user.getId() for user in api.user.get_users(groupname=groupname)]
            # Only include members who are also in attendees
            groups_with_attendees[group_title] = [u for u in group_members if u in attendees]

        return groups_with_attendees

    
    

    
 
    