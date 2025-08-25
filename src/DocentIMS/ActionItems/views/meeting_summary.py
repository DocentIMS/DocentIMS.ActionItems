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
    
    
    @property
    def get_groups(self):
        # alsoProvides(self.request, IDisableCSRFProtection)
        attendees_groups = self.context.attendees_group
        if  attendees_groups and attendees_groups != None:
            groups = []
            for group in attendees_groups:
                group_this = api.group.get(groupname=group)
                groups.append(group_this.getGroupTitleOrName())
                
            return ", ".join(groups)
        
        return None
    
    
    
    @property
    def get_grouped_attendees(self):
        """
        Returns a dictionary with:
        {
            'in_groups': ['user1', 'user2', 'user3'],
            'not_in_groups': ['user4', 'user5']
        }
        """
        attendees = set(self.get_attendees)
        users_in_groups = set()

        for groupname in self.context.attendees_group or []:
            group = api.group.get(groupname=groupname)
            if not group:
                continue
            group_members = [user.getId() for user in api.user.get_users(groupname=groupname)]
            users_in_groups.update([u for u in group_members if u in attendees])

        not_in_groups = attendees - users_in_groups

        return {
            'in_groups': list(users_in_groups),
            'not_in_groups': list(not_in_groups)
        }

    # def get_groups_with_attendees(self):
    #     """
    #     Returns a list with dictionary:
         
    #     """
    #     attendees = set(self.get_attendees)
    #     groups_with_attendees = []

    #     for groupname in self.context.attendees_group or []:
    #         group = api.group.get(groupname=groupname)
    #         if not group:
    #             continue
    #         group_title = group.getGroupTitleOrName()
    #         group_members = [user.getId() for user in api.user.get_users(groupname=groupname)]
    #         # Only include members who are also in attendees
    #         groups_with_attendees.append({'groupname': group_title ,'users': [u for u in group_members if u in attendees]})

    #     return groups_with_attendees

    
    
    

    
 
    