# -*- coding: utf-8 -*-
from plone.dexterity.content import Item
from plone.supermodel import model
# from plone import api
from datetime import datetime
from zope import schema
from zope.interface import implementer
# from plone.dexterity.content import Container
# from plone.autoform import directives as form
 
    

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
    
    # form.mode(title='hidden')  # Hide the title field from the form
    # title = schema.TextLine(
    #     title=u"Title",
    #     description=u"This is a computed field.",
    #     required=False,
    #     readonly=True
    # )
    
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
    
    # meeting_date_time = schema.Date(
    #     description=u"Scheduled meeting time",
    #     required=False,
    #     title=u"Meeting Date"
    # )

    # call_to_order= schema.Time(
    #     required=False,
    #     title="Call to Order"
    # )
 
 
 
@implementer(IMeetingNotes)
class MeetingNotes(Item):
    """
    """
        
    def Title(self):
        # Example: compute the title based on the description field or other logic
        return 'Something'