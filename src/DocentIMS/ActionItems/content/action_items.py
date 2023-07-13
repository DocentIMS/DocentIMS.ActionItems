# -*- coding: utf-8 -*-
from plone.dexterity.content import Container
from plone.supermodel import model

import plone.api


class IActionItems(model.Schema):
    """ Marker interface for ActionItems
    """
    
    #def Description(self, context):
    #    return 'My overriden description'

    #def getDescription(self, context):
    #    return 'My overriden description'
