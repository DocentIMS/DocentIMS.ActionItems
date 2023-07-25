# -*- coding: utf-8 -*-
"""Module where all interfaces, events and exceptions live."""

from zope.publisher.interfaces.browser import IDefaultBrowserLayer
from z3c.form import interfaces
from zope import schema
from zope.interface import alsoProvides
from plone.supermodel import model
from collective.z3cform.datagridfield.datagridfield import DataGridFieldFactory
from collective.z3cform.datagridfield.registry import DictRow
from plone.autoform.directives import widget
from medialog.controlpanel.interfaces import IMedialogControlpanelSettingsProvider

from zope.i18nmessageid import MessageFactory
_ = MessageFactory('DocentIMS.ActionItems')


class IDocentimsActionitemsLayer(IDefaultBrowserLayer):
    """Marker interface that defines a browser layer."""

class IVocabulari(model.Schema):
    vocabulary_entry = schema.Text(
        title=_(u'Vocabulary', 'Vocabulary'),
        required=False,
        default=u"""One on each line"""
    )

class IDocentimsSettings(model.Schema):
    """Adds settings to medialog.controlpanel
    """

    model.fieldset(
        'vocabularies',
        label=_(u'Vocabularies'),
        fields=[
            'vokabularies',
            ],
        )

    model.fieldset(
        'project',
        label=_(u'Project Information'),
        fields=[
            'project_title',
            'project_description',
            'project_full_name',
            'project_short_name',
            'project_contract_number',
            'project_document_naming_convention'
            ],
        )


    model.fieldset(
        'Company',
        label=_(u'Company Information'),
        fields=[
            'full_company_name',
            'short_company_name',
            'company_letter_code',
            'company_role',
            'company_logo',
            ],
        )

    model.fieldset(
        'address',
        label=_(u'Address'),
        fields=[
            'company_full_street_address',
            'company_city',
            'company_other_address',
            'company_state',
            'company_zip',
            'company_main_phone_number',
            ],
        )



    project_title = schema.TextLine(
        required = False,
        title=_(u"label_title", default=u"Project Title"),
        description=_(u"help_title",
                      default=u"Project title")
        )
    project_description = schema.TextLine(
        required = False,
        title=_(u"label_project_description", default=u"Project Description"),
        description=_(u"help_project_description",
                      default=u"Project description")
        )
    project_full_name = schema.TextLine(
        required = False,
        title=_(u"label_project_fullname", default=u"Project Full Name"),
        description=_(u"help_project_fullname",
                      default=u"Project_fullname")
        )
    project_short_name = schema.TextLine(
        required = False,
        title=_(u"label_project_short_name", default=u"Project Short name"),
        description=_(u"help_project_short_name",
                      default=u"Project_short_name")
        )
    project_contract_number = schema.TextLine(
        required = False,
        title=_(u"label_project_contract_number", default=u"Project Contract Number"),
        description=_(u"help_project_contract_number",
                      default=u"Project_contract_number")
        )
    project_document_naming_convention = schema.TextLine(
        required = False,
        title=_(u"label_project_document_naming_convention", default=u"Project Document Naming Convention"),
        description=_(u"help_project_document_naming_convention",
                      default=u"Project document naming convention")
        )

    full_company_name = schema.TextLine(
        required = False,
        title=_(u"label_company_name", default=u"Full Company Name")
        )
    short_company_name= schema.TextLine(
        required = False,
        title=_(u"label_company_short_name", default=u"Short Company Name")
        )
    company_letter_code = schema.TextLine(
        required = False,
        title=_(u"label_company_letter_code", default=u"Company 3-letter code")
        )
    company_role = schema.Text(
        required = False,
        title=_(u"label_company_role", default=u"Company role")
        )
    company_logo = schema.Text(
        required = False,
        title=_(u"label_company_logo", default=u"Company Logo")
        )


    company_full_street_address = schema.Text(
        required = False,
        title=_(u"label_company_full_street_adress", default=u"Full Street Address")
        )
    company_city = schema.TextLine(
        required = False,
        title=_(u"label_company_citye", default=u"City")
        )
    company_other_address = schema.Text(
        required = False,
        title=_(u"label_company_other_adress", default=u"Other Address")
        )
    company_state = schema.TextLine(
        required = False,
        title=_(u"label_company_state", default=u"State")
        )
    company_zip = schema.TextLine(
        required = False,
        title=_(u"label_company_zip", default=u"ZIP")
        )
    company_main_phone_number = schema.TextLine(
        required = False,
        title=_(u"label_main_phone_number", default=u"Main Phone Number")
        )


    widget(vokabularies=DataGridFieldFactory)
    vokabularies = schema.List(
        title = _(u"Vocabularies",
            default=u"Ekstra buttons"),
        value_type=DictRow(schema=IVocabulari),
    )



alsoProvides(IDocentimsSettings, IMedialogControlpanelSettingsProvider)
