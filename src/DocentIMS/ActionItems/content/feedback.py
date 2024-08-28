# -*- coding: utf-8 -*-
from plone.dexterity.content import Item
from plone.supermodel import model
from plone.autoform import directives

from plone.app.z3cform.widget import AjaxSelectFieldWidget
from zope import schema


class IFeedback(model.Schema):
    """ Marker interface for Feedback
    """
    
    submitted_by = schema.TextLine(
        title= "Who submitted this feedback?",
        required=False,
    )
    directives.widget("submitted_by",  AjaxSelectFieldWidget,  allowMulti=False, vocabulary= 'DocentIMS.ActionItems.FullnamesVocabulary',  klass="event_attends")
