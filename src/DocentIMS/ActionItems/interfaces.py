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
from plone.app.textfield import RichText

from medialog.controlpanel.interfaces import IMedialogControlpanelSettingsProvider
from plone.app.z3cform.widget import SelectFieldWidget

#from z3c.form import validator

#from  zope import interface
#from zope.interface import invariant, Invalid 

from zope.schema.interfaces import  InvalidValue

#from Products.statusmessages.interfaces import IStatusMessage
from plone.api.portal import show_message

#from plone.namedfile.field import NamedBlobImage
from plone.namedfile import field

from zope.i18nmessageid import MessageFactory
_ = MessageFactory('DocentIMS.ActionItems')


def richtextConstraint(value):
    """ Workaround for bug 
    """
    #import pdb; pdb.set_trace()
    value = value.output
    return True 

def richtextget(value):
    """ Workaround for bug 
    """
    #import pdb; pdb.set_trace()
    value = value.output
    return value 

def company_letter_kodeConstraint(value):
    """Check that the company_3 letter code is upperclass
    """
    if value != None and value != '':
        if len(value) != 3:
             raise InvalidValue()
             #Works with datagridfield, but will show error message 'Constraint not satisfied /The system could not process the given value.'
             return True
        
        if not value.isupper():
            raise  InvalidValue("Only capital letters for Company 3 letter code")
            return True
    return True

def stateConstraint(value):
    """Check lenght = 2 and upperclass
    """
    if value != None and value != '':
        if len(value) != 2:
             raise InvalidValue()
             #Works with datagridfield, but will show error message 'Constraint not satisfied /The system could not process the given value.'
             return True
        if not value.isupper():
            # Raises error, but do not 'render the text'
            raise  InvalidValue("Only 2 capital letters for State")
            return True
        if not value in [ 'AL', 'AK', 'AZ', 'AR', 'CA', 'CO', 'CT', 'DE', 'FL', 'GA', 'HI', 'ID', 'IL', 'IN', 'IA', 'KS', 'KY', 
                        'LA', 'ME', 'MD', 'MA', 'MI', 'MN', 'MS', 'MO', 'MT', 'NE', 'NV', 'NH', 'NJ', 'NM', 'NY', 'NC', 'ND', 
                        'OH', 'OK', 'OR', 'PA', 'RI', 'SC', 'SD', 'TN', 'TX', 'UT', 'VT', 'VA', 'WA', 'WV', 'WI', 'WY']:
            
            show_message(message="Company State does not exist", type='warning')
            #raise InvalidValue()
            #return True

    return True


class IDocentimsActionitemsLayer(IDefaultBrowserLayer):
    """Marker interface that defines a browser layer."""

class IVocabulari(model.Schema):
    vocabulary_entry = schema.TextLine(
        title=_(u'Vocabulary entries', 'Vocabulary entries'),
        required=False,
    )

class ITableRows(model.Schema):
    widget(row_field=SelectFieldWidget)
    row_field = schema.Choice(
        vocabulary=u"DocentIMS.ActionItems.AiFieldsVocabulary",
        title=_(u"Field", default=u"Field"),
        required=False,
    )

    row_title = schema.TextLine(
        title=_(u'Table title', 'Table title'),
        required=False,
    )

class IScopeTableRows(model.Schema):
    widget(row_field=SelectFieldWidget)
    row_field = schema.Choice(
        vocabulary=u"DocentIMS.ActionItems.SowFieldsVocabulary",
        title=_(u"Field", default=u"Field"),
        required=False,
    )

    row_title = schema.TextLine(
        title=_(u'Table title', 'Table title'),
        required=False,
    )



class ICompany(model.Schema):
    full_company_name = schema.TextLine(
        required = False,
        title=_(u"label_company_name", default=u"Full Company Name")
        )
    short_company_name= schema.TextLine(
        required = False,
        title=_(u"label_company_short_name", default=u"Short Company Name")
        )
    company_letter_kode = schema.TextLine(
        required = False,
        title=_(u"label_company_letter_code", default=u"Company 3-letter code"),
        constraint=company_letter_kodeConstraint,
        )


    company_role = schema.Text(
        required = False,
        title=_(u"label_company_role", default=u"Company role")
        )
    #company_logo = schema.Text(
    #    required = False,
    #    title=_(u"label_company_logo", default=u"Company Logo")
    #    )

    #company_logo = field.NamedBlobImage(title=u"Company Logo")


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
        title=_(u"label_company_state", default=u"State"),
        constraint=stateConstraint,
        )

#TO DO, maybe use a choice field instead ?

# Alabama: AL
# Alaska: AK
# Arizona: AZ
# Arkansas: AR
# California: CA
# Colorado: CO
# Connecticut: CT
# Delaware: DE
# Florida: FL
# Georgia: GA
# Hawaii: HI
# Idaho: ID
# Illinois: IL
# Indiana: IN
# Iowa: IA
# Kansas: KS
# Kentucky: KY
# Louisiana: LA
# Maine: ME
# Maryland: MD
# Massachusetts: MA
# Michigan: MI
# Minnesota: MN
# Mississippi: MS
# Missouri: MO
# Montana: MT
# Nebraska: NE
# Nevada: NV
# New Hampshire: NH
# New Jersey: NJ
# New Mexico: NM
# New York: NY
# North Carolina: NC
# North Dakota: ND
# Ohio: OH
# Oklahoma: OK
# Oregon: OR
# Pennsylvania: PA
# Rhode Island: RI
# South Carolina: SC
# South Dakota: SD
# Tennessee: TN
# Texas: TX
# Utah: UT
# Vermont: VT
# Virginia: VA
# Washington: WA
# West Virginia: WV
# Wisconsin: WI
# Wyoming: WY



    company_zip = schema.TextLine(
        required = False,
        title=_(u"label_company_zip", default=u"ZIP")
    )
    #company_main_phone_number = schema.TextLine(
    #    required = False,
    #    title=_(u"label_main_phone_number", default=u"Main Phone Number")
    #    )




class IDocentimsSettings(model.Schema):
    """Adds settings to medialog.controlpanel
    """

    model.fieldset(
        'project',
        label=_(u'Project Information'),
        fields=[
            'project_title',
            'project_short_name',
            'project_description',
            # 'project_companies',
            'project_contract_number',
            'project_document_naming_convention'
            ],
        )

    model.fieldset(
        'vocabularies',
        label=_(u'Vocabularies'),
        fields=[
            'vokabularies',
            # 'vokabularies2',
        ] 
    )

    model.fieldset(
        'notifications',
        label=_(u'Notifications'),
        fields=[
            'future_green',
            'soon_yellow',
             'urgent_red',
            ],
        )
    # model.fieldset(
    #     'Company',
    #     label=_(u'Company Information'),
    #     fields=[
    #         'full_company_name',
    #         'short_company_name',
    #         'company_letter_code',
    #         'company_role',
    #         'company_logo',
    #         ],
    #     )

    # model.fieldset(
    #     'address',
    #     label=_(u'Address'),
    #     fields=[
    #         'company_full_street_address',
    #         'company_city',
    #         'company_other_address',
    #         'company_state',
    #         'company_zip',
    #         ],
    #     )


    model.fieldset(
        'companies',
        label=_(u'Companies'),
        fields=[
            'companies',
            ],
        )

    model.fieldset(
        'table',
        label=_(u'Action Items Columns'),
        fields=[
            'table_columns',
            ],
        )
    
    model.fieldset(
        'scope_table',
        label=_(u'Scope table Columns'),
        fields=[
            'scope_table_columns',
            ],
        )

    project_title = schema.TextLine(
        required = False,
        title=_(u"label_title", default=u"Project Title"),
        description=_(u"help_title",
                      default=u"Enter short project title")
        )

    #project_full_name = schema.TextLine(
    #    required = False,
    #    title=_(u"label_project_fullname", default=u"Project Full Name"),
    #    description=_(u"help_project_fullname",
    #                  default=u"Project_fullname"),
    #    )

    project_short_name = schema.TextLine(
        title=_(u"label_project_short_name",
        default=u"Project Short name"),
        description=_(u"help_project_short_name",
                      default=u"Project_short_name")
        )
    

    # project_description = RichText(
    #     title=u"Project Description Rich text",
    #     required=False, 
    # )

    widget("project_description", klass="pat-tinymce")
    project_description = schema.Text(
        required = False,
        title=_(u"label_project_description", default=u"Project Description"),
        description=_(u"help_project_description",
                      default=u"Project description")
        )

    # project_companies = schema.Choice(
    #     required = False,
    #     vocabulary=u"DocentIMS.ActionItems.CompanyVocabulary",
    #     title=_(u"label_project_companies", default=u"Project Companies"),
    #     description=_(u"help_project_companies",
    #                   default=u"Project Companies List")
    #     )


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
    
    urgent_red = schema.Int(
        title=_(u"label_red", default=u"Urgent Red value"),
        description="enter number of days",
        )
    
    future_green = schema.Int(
        title=_(u"label_green", default=u"Future Green value"),
        description="enter number of days",
        )

    soon_yellow = schema.Int(
        title=_(u"label_yellow", default=u"Soon Yellow value"),
        description="enter number of days",
        )

    # full_company_name = schema.TextLine(
    #     required = False,
    #     title=_(u"label_company_name", default=u"Full Company Name")
    #     )
    # short_company_name= schema.TextLine(
    #     required = False,
    #     title=_(u"label_company_short_name", default=u"Short Company Name")
    #     )
    # company_letter_code = schema.TextLine(
    #     required = False,
    #     max_length=3,
    #     min_length=3,
    #     title=_(u"label_company_letter_code", default=u"Company 3-letter code"),
    #     constraint=company_letter_codeConstraint,
    #     )

    # company_role = schema.Text(
    #     required = False,
    #     title=_(u"label_company_role", default=u"Company role")
    #     )
    # company_logo = schema.Text(
    #     required = False,
    #     title=_(u"label_company_logo", default=u"Company Logo")
    # )

    # #company_logo = field.NamedBlobImage(title=u"Company Logo")


    # company_full_street_address = schema.Text(
    #     required = False,
    #     title=_(u"label_company_full_street_adress", default=u"Full Street Address")
    #     )
    # company_city = schema.TextLine(
    #     required = False,
    #     title=_(u"label_company_citye", default=u"City")
    #     )

    # company_other_address = schema.Text(
    #     required = False,
    #     title=_(u"label_company_other_adress", default=u"Other Address")
    #     )
    # company_state = schema.TextLine(
    #     required = False,
    #     title=_(u"label_company_state", default=u"State")
    #     )
    # company_zip = schema.TextLine(
    #     required = False,
    #     title=_(u"label_company_zip", default=u"ZIP")
    # )

    #company_main_phone_number = schema.TextLine(
    #    required = False,
    #    title=_(u"label_main_phone_number", default=u"Main Phone Number")
    #    )


    widget(vokabularies=DataGridFieldFactory)
    vokabularies = schema.List(
        title = _(u"Team Member Project Roles",
            default=u"Team Member Project Roles"),
        value_type=DictRow(schema=IVocabulari),
        required=False,
    )

    # widget(vokabularies2=DataGridFieldFactory)
    # vokabularies2 = schema.List(
    #     title = _(u"Vocabularies 2",
    #         default=u"Vocabulary 2"),
    #     value_type=DictRow(schema=IVocabulari),
    #     required=False,
    # )

    widget(companies=DataGridFieldFactory)
    companies = schema.List(
        title = _(u"Companies",
            default=u"Companies"),
        value_type=DictRow(schema=ICompany),
    )

    widget(table_columns=DataGridFieldFactory)
    table_columns = schema.List(
        title = _(u"Table Columns",
            default=u"Table Column fields to be used for actions overview Table / View"),
            value_type=DictRow(schema=ITableRows),
    )

    widget(scope_table_columns=DataGridFieldFactory)
    scope_table_columns = schema.List(
        title = _(u"Table Columns",
            default=u"Table Column fields to be used for Scope  Table / View"),
            value_type=DictRow(schema=IScopeTableRows),
    )

    #table_columns = schema.List(
    #    title = _(u"Table Columns",
    #        default=u"Table Column fields"),
    #        value_type=schema.Choice(vocabulary=u"DocentIMS.ActionItems.AiFieldsVocabulary"),
    #)

alsoProvides(IDocentimsSettings, IMedialogControlpanelSettingsProvider)
