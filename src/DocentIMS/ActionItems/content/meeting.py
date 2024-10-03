# -*- coding: utf-8 -*-
from plone.dexterity.content import Item
from plone.supermodel import model


class IMeeting(model.Schema):
    """ Marker interface for Meeting
    """

    # @property
    # def getTitle(self):
    #     """Get the title based on something"""
    #     # return self.Title()
    #     return 'Random Title'
