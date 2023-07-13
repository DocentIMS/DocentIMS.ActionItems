# -*- coding: utf-8 -*-
"""Module where all interfaces, events and exceptions live."""

from zope.publisher.interfaces.browser import IDefaultBrowserLayer
from z3c.form import interfaces
from zope import schema
from zope.interface import alsoProvides
#from plone.directives import form
from plone.supermodel import model
#from plone.autoform.directives import widget

from medialog.controlpanel.interfaces import IMedialogControlpanelSettingsProvider

from zope.i18nmessageid import MessageFactory
_ = MessageFactory('DocentIMS.ActionItems')


class IDocentimsActionitemsLayer(IDefaultBrowserLayer):
    """Marker interface that defines a browser layer."""



class IDocentimsSettings(model.Schema):
    """Adds settings to medialog.controlpanel
    """

    model.fieldset(
        'project',
        label=_(u'Project Information'),
        fields=[
            'my_field',
            ],
        )


    model.fieldset(
        'Company',
        label=_(u'Company Information'),
        fields=[
            'm_y_field',
            ],
        )

    model.fieldset(
        'vocabularies',
        label=_(u'Vocabularies'),
        fields=[
            'vokabulary',
            ],
        )

    my_field = schema.TextLine(
        title=_(u"label_my_field", default=u"My Field"),
        description=_(u"help_my_field",
                      default=u"My description")
        )

    m_y_field = schema.TextLine(
        title=_(u"label_my_2_field", default=u"My 2 Field"),
        description=_(u"help_my_2_field",
                      default=u"My 2 description")
        )

    vokabulary = schema.Text(
        title=_(u"label_vokabulary", default=u"Vokaculary 1"),
        description=_(u"help_vocabulary",
                      default=u"One entry on each line")
        )


alsoProvides(IDocentimsSettings, IMedialogControlpanelSettingsProvider)
