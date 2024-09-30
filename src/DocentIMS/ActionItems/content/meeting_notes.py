# -*- coding: utf-8 -*-
from plone.dexterity.content import Item
from plone.supermodel import model
 
from plone import api
from datetime import datetime
from zope import schema
from plone.supermodel import model
from zope.interface import implementer
# from plone.dexterity.content import Container
from plone.supermodel import model


    
    

def default_title():
    """Return default title 'Notes <Date>' where Date is today's date."""
    today = datetime.today().strftime('%Y-%m-%d')
    return f"Notes {today}"

def default_description():
    """Return default description."""
    return f"Notes taken during the meeting"

class IMeetingNotes(model.Schema):
    """ Marker interface for MeetingNotes
    """
    
    model.load("meeting_notes.xml")
    
    title = schema.TextLine(
        title=u"Title",
        required=True,
        defaultFactory=default_title
    )
    
    description = schema.TextLine(
        title=u"Description",
        required=True,
        defaultFactory=default_description
    )
    

      
    
 