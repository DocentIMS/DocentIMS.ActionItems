# -*- coding: utf-8 -*-
from plone.dexterity.content import Item
from plone.supermodel import model


class IMeeting(model.Schema):
    """ Marker interface for Meeting
    """
    
    # def default_title():
    #     """Return default title 'Notes <Date>' where Date is today's date."""
    #     today = datetime.today().strftime('%Y-%m-%d')
    #     return f"Notes {today}"

    # @property
    # def getTitle(self):
    #     """Get the title based on something"""
    #     # return self.Title()
    #     return 'Random Title'
