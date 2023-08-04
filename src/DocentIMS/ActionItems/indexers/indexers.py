# -*- coding: utf-8 -*-

from plone.app.contenttypes.interfaces import IDocument
from plone.dexterity.interfaces import IDexterityContent
from plone.dexterity.interfaces import IDexterityContainer
from plone.indexer import indexer
#import DateTime
import datetime
#from datetime import timezone

@indexer(IDexterityContent)
def dummy(obj):
    """ Dummy to prevent indexing other objects thru acquisition """
    raise AttributeError('This field should not indexed here!')


@indexer(IDexterityContainer)  # ADJUST THIS!
def actionIndexer(obj):
    """Calculate and return the value for the indexer"""
    #import pdb; pdb.set_trace()
    if "action_items-" in obj.id:
        action_item =  obj.id.replace('action_items', '').replace("-", '')
        action_item_no = int(float(action_item))
        return action_item_no
    return None


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
def daysleftIndexer(obj):
    """Calculate and return the value for the indexer"""
    due_date = obj.duedate or None
    # difference between dates in timedelta
    if due_date != None:
        delta = due_date - datetime.date.today()
        if delta.days<1:
            return '0 - Out of time'
        if delta.days<=7:
            return '1 – Less than 7'
        if delta.days<=14:
            return '2 - Less than 14'

        return '3 - More than 15'

    return None
