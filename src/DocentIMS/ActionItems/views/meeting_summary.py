# -*- coding: utf-8 -*-

from plone.app.event.browser.event_summary import EventSummaryView

# from DocentIMS.ActionItems import _

from Acquisition import aq_parent
from plone.app.event import _
from plone.event.interfaces import IEventAccessor
from plone.event.interfaces import IOccurrence
from plone.event.interfaces import IRecurrenceSupport
from plone.memoize import view
from plone.uuid.interfaces import IUUID
from Products.CMFCore.utils import getToolByName
from Products.Five.browser import BrowserView
from zope.component import getMultiAdapter
from zope.contentprovider.interfaces import IContentProvider
from plone import api


class MeetingSummaryView(EventSummaryView):
    
    # @property
    def get_attendees(self):
        attendees = list(self.data.attendees)
        attendees_groups = self.context.attendees_group
        # if  attendees_groups:
        for meeting_group in attendees_groups:
                groupmembers = api.user.get_users(groupname=meeting_group)
                for groupmember in groupmembers:
                    attendees.append(groupmember.getId())
                    
        return tuple(attendees)
    