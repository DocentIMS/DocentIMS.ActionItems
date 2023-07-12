# -*- coding: utf-8 -*-

# from DocentIMS.ActionItems import _
from Products.Five.browser import BrowserView
from zope.interface import Interface
from plone import api
import DateTime
import datetime


class IActionItemsView(Interface):
    """ Marker Interface for IActionItemsView"""


class ActionItemsView(BrowserView):

    def portal_url(self):
        return api.portal.get().absolute_url()

    def due_date(self):
        #return self.context.created().ISO()
        #return datetime.datetime.from_date(initial_due_date).ISO()
        return self.context.initial_due_date().ISO()

    def days_left(self):
        # to do, due date or initial due date ?
        due_date = self.context.revised_due_date or  self.context.initial_due_date or None

        # difference between dates in timedelta
        delta = due_date - datetime.date.today()
        return delta.days
        #days = delta.days

        #if days > -1:
        #    days




    def source_relations(self):
        relations =  api.relation.get(source=self.context)
        return relations

    def target_relations(self):
        relations =  api.relation.get(target=self.context)
        return relations

    def new_id(self):
        if self.context.id == 'action_items':
            return 'South Tacoma Station – 0'
        return  self.context.id.replace('action_items-', 'South Tacoma Station – ')

    def get_sow(self):
        #import pdb; pdb.set_trace()
        if self.context.related_sow_section:
            return api.content.get(UID=self.context.related_sow_section)
        return None

    def get_sow_text(self):
        if self.context.related_sow_section:
            rel_sow = api.content.get(UID=self.context.related_sow_section)
            return rel_sow.bodytext.output
        return None

    def get_creator(self):
        member = api.user.get(userid=self.context.Creator())
        return  {'id': member.getProperty('id'),
                  'last_name': member.getProperty('last_name'),
                  'first_name': member.getProperty('first_name'),
                  'company': member.getProperty('location'),
                 }

    def get_owner(self):
        member = api.user.get(userid=self.context.assigned_to)

        if member:
            return  {'id': member.getProperty('id'),
                  'last_name': member.getProperty('last_name'),
                  'first_name': member.getProperty('first_name'),
                  'company': member.getProperty('location'),
                 }
        return None
