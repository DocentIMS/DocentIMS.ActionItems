# -*- coding: utf-8 -*-

# from DocentIMS.ActionItems import _
from Products.Five.browser import BrowserView
from zope.interface import Interface

# -*- coding: utf-8 -*-

from plone import api
import DateTime
import numpy as np
import datetime
import holidays
from DocentIMS.ActionItems.interfaces import IDocentimsSettings


class ISowView(Interface):
    """ Marker Interface for ISowView"""


class SowView(BrowserView):
    # If you want to define a template here, please remove the template from
    # the configure.zcml registration of this view.
    # template = ViewPageTemplateFile('sow_view.pt')

    def __call__(self):
        # Implement your own actions:
        return self.index()

    def portal_url(self):
        return api.portal.get().absolute_url()

    def due_date(self):
        #return self.context.created().ISO()
        #return datetime.datetime.from_date(initial_due_date).ISO()
        return self.context.initial_due_date().ISO()

    def days_left(self):
        # to do, due date or initial due date ?
        #due_date = self.context.duedate or None
        due_date = self.context.revised_due_date or self.context.initial_due_date or None

        # difference between dates in timedelta
        if due_date != None:
            delta = due_date - datetime.date.today()
            #if delta.days <= red_value:
            #    set flag to tru 
            #if delta.days <= 0:
            #    self.context.is_this_item_closed == True
            
            return delta.days
            
        return None
        #days = delta.days

        #if days > -1:
        #    days
        
        
    def workdays_left(self):
        due_date = self.context.revised_due_date or self.context.initial_due_date or None

        # difference between dates in timedelta
        if due_date != None:
             
            today = datetime.date.today()
            usholiday =   holiday_dates = [key for key in holidays.US(years=[today.year, today.year+1])]
            workdays = np.busday_count(today, due_date, holidays = usholiday)
            return workdays

        return None
            

    def get_css_urgency(self):
        daycount = self.workdays_left() or None

        if daycount:

            if daycount <=   api.portal.get_registry_record('urgent_red', interface=IDocentimsSettings):
                return 'urgent_red'

            if daycount <=   api.portal.get_registry_record('soon_yellow', interface=IDocentimsSettings):
                return 'soon_yellow'

            if daycount <=   api.portal.get_registry_record('future_green', interface=IDocentimsSettings):
                return 'future_green'

        return 'long_grey'


    def source_relations(self):
        relations =  api.relation.get(source=self.context)
        return relations

    def target_relations(self):
        relations =  api.relation.get(target=self.context)
        return relations


    def get_creator(self):
        member = api.user.get(userid=self.context.Creator())
        company = ''
        company_id =  member.getProperty('company')
        if company_id != None:
            company_obj = api.content.get(UID=company_id)
            NoneType = type(None)
            if not isinstance(company_obj, NoneType):
                company = company_obj.Title()
        return  {'id': member.getProperty('id'),
                  'last_name': member.getProperty('last_name'),
                  'first_name': member.getProperty('first_name'),
                  'company': company,
                 }

    def get_owner(self):
        member = api.user.get(userid=self.context.assigned_to)
        if member:
            company_id =  member.getProperty('company')
             
            #if company_id:
            #    company = api.content.get(UID=company_id).Title()
            return  {'id': member.getProperty('id'),
                  'last_name': member.getProperty('last_name'),
                  'first_name': member.getProperty('first_name'),
                  'company': company_id,
                 }
        return None
    
    def get_duedate(self):
        return self.context.revised_due_date or self.context.initial_due_date or None




