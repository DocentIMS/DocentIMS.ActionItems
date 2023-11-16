# -*- coding: utf-8 -*-
from plone.dexterity.content import Item
from plone.app.textfield import RichText
from plone.supermodel import model


class IFrontPage(model.Schema):
    """ Marker interface for FrontPage
    """
    
    frontpage_richtext = RichText(
        title=u"Project Frontpage logged in text",
        required=False, 
    )
