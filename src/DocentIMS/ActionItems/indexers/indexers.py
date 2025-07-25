# -*- coding: utf-8 -*-

from plone.app.contenttypes.interfaces import IDocument
from plone.dexterity.interfaces import IDexterityContent
from plone.dexterity.interfaces import IDexterityContainer
from plone.indexer import indexer
#import DateTime
#import datetime
#from datetime import timezone
from plone import api
import DateTime
import numpy as np
import datetime
import holidays
from DocentIMS.ActionItems.interfaces import IDocentimsSettings


@indexer(IDexterityContent)
def dummy(obj):
    """ Dummy to prevent indexing other objects thru acquisition """
    raise AttributeError('This field should not indexed here!')


@indexer(IDexterityContent)
def dummy(obj):
    """ Dummy to prevent indexing other objects thru acquisition """
    raise AttributeError('This field should not indexed here!')

@indexer(IDexterityContainer)  # ADJUST THIS!
def assigned_idIndexer(obj):
    """Index id instead of assigned_to"""
    u_id = obj.assigned_to
    
    if not u_id:
        return "unassigned"
    
    return u_id

@indexer(IDexterityContainer)  # ADJUST THIS!
def assigned_toIndexer(obj):
    """Index real name instead of username for assigned_to"""
    username = obj.assigned_to
    
    if not username:
        return 'Unassigned'
    
    if username:
        fullname = api.user.get(userid=username).getProperty('fullname')
        if fullname:
            return fullname 
    return username



@indexer(IDexterityContainer)  # ADJUST THIS!
def attendeesIndexer(obj):
    """Calculate and return the value for the indexer"""
    if obj.portal_type in  ['Meeting', 'meeting']:
        attendees = obj.attendees
        groups = obj.attendees_group
        if groups and groups != None:
            all_users = list(attendees)
            for group in groups:
                 groupmembers = api.user.get_users(groupname=group)
                 if groupmembers and groupmembers != None:
                     for groupmember in groupmembers:
                        all_users.append(groupmember.getId())
                         
            return tuple(all_users)
        
        return attendees




@indexer(IDexterityContainer)  # ADJUST THIS!
def actionIndexer(obj):
    """Calculate and return the value for the indexer"""
    #import pdb; pdb.set_trace()
    if "action_items-" in obj.id:
        action_item =  obj.id.replace('action_items', '').replace("-", '')
        action_item_no = int(float(action_item))
        return action_item_no
    return int(0)


@indexer(IDexterityContainer)  # ADJUST THIS!
def duedateIndexer(obj):
    """Calculate and return the value for the indexer"""
    value = obj.revised_due_date or obj.initial_due_date or None
    if value:
        obj.duedate = value
        return value
    return None


@indexer(IDexterityContainer)  # ADJUST THIS!
def priorityIndexer(obj):
    """Calculate and return the value for the indexer"""
    if obj.priority:
        return int(float(obj.priority))
    return None

@indexer(IDexterityContainer)  # ADJUST THIS!
def prioritystringIndexer(obj):
    """Calculate and return the value for the indexer"""
    if obj.priority:
        obj.prioritystring = str(obj.priority)
        return str(obj.priority)
    return None


@indexer(IDexterityContainer)  # ADJUST THIS!
def closedIndexer(obj):
    """Calculate and return the value for the indexer"""
    if obj.is_this_item_closed:
        obj.closed = 'Yes'
        return 'Yes'
    return 'No'


@indexer(IDexterityContainer)  # ADJUST THIS!
def is_this_action_out_of_the_scope_of_work_Indexer(obj):
    """Calculate and return the value for the indexer"""
    if obj.is_this_action_out_of_the_scope_of_work_:
        obj.is_this_action_out_of_the_scope_of_work_ = 'Yes'
        return 'Yes'
    return 'No'


@indexer(IDexterityContainer)  # ADJUST THIS!
def daysleftIndexer(obj):
    """Calculate and return the value for the indexer"""
    due_date = obj.duedate or None
    # difference between dates in timedelta
    if due_date != None:
        #import pdb; pdb.set_trace()
        today = datetime.date.today()
        usholiday =   holiday_dates = [key for key in holidays.US(years=[today.year, today.year+1])]
        workdays = np.busday_count(today, due_date, holidays = usholiday)

        return str(workdays)

    return None


@indexer(IDexterityContainer)  # ADJUST THIS!
def urgencyIndexer(obj):
    """Calculate and return the value for the indexer"""
    due_date = obj.duedate or None
    if due_date != None:
        #import pdb; pdb.set_trace()
        today = datetime.date.today()
        usholiday =   holiday_dates = [key for key in holidays.US(years=[today.year, today.year+1])]
        workdays = np.busday_count(today, due_date, holidays = usholiday)

        red = api.portal.get_registry_record('urgent_red', interface=IDocentimsSettings)
        yellow = api.portal.get_registry_record('soon_yellow', interface=IDocentimsSettings)
        green = api.portal.get_registry_record('future_green', interface=IDocentimsSettings)
        
        if workdays <=   red:
            return "Urgent < {days} workdays".format(days = red)

        if workdays <=   yellow:
            return "Soon < {days} workdays".format(days = yellow) 

        if workdays <=   green:
            return "Future < {days} workdays".format(days = green) 

        return "More than {days} workdays".format(days = green) 

    return "Unset"



@indexer(IDexterityContainer)  # ADJUST THIS!
def stoplightIndexer(obj):
    """Calculate and return the value for the indexer"""
    due_date = obj.duedate or None
    if due_date != None:
        today = datetime.date.today()
        usholiday =   holiday_dates = [key for key in holidays.US(years=[today.year, today.year+1])]
        workdays = np.busday_count(today, due_date, holidays = usholiday)

        red = api.portal.get_registry_record('urgent_red', interface=IDocentimsSettings)
        yellow = api.portal.get_registry_record('soon_yellow', interface=IDocentimsSettings)
        green = api.portal.get_registry_record('future_green', interface=IDocentimsSettings)
        
        if workdays <=   red:
            return "Red"

        if workdays <=   yellow:
            return "Yellow" 

        if workdays <=   green:
            return "Green"

        return "Gray"

    return "Unset"