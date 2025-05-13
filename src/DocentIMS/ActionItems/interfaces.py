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
from plone.app.z3cform.widgets.richtext import RichTextFieldWidget
from plone.registry.field import PersistentField
from medialog.controlpanel.interfaces import IMedialogControlpanelSettingsProvider
from plone.app.z3cform.widget import SelectFieldWidget, SelectWidget
from collective.z3cform.colorpicker.colorpicker  import ColorpickerFieldWidget
from zope.schema.interfaces import  InvalidValue
from plone.api.portal import show_message
from plone.namedfile import field
from plone.app.contentrules.handlers  import execute_user_rules
from plone.app.z3cform.widget import AjaxSelectFieldWidget



from zope.i18nmessageid import MessageFactory
_ = MessageFactory('DocentIMS.ActionItems')




class RichTextFieldRegistry(PersistentField, RichText):
    """ persistent registry textfield """


def richtextConstraint(value):
    """ Workaround for bug 
    """
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

# class IColorForm(model.Schema):
#     color = Color(
#         title=u"Color",
#         description=u"",
#         required=False,
#         default="#ff0000"
#     )

class IVocabulari(model.Schema):
    vocabulary_entry = schema.TextLine(
        title=_(u'Vocabulary entries', 'Team Roles'),
        description=u"Each team member will be assigned a “Role” during their membership creation.  The role for each member must be created here before their account can be created.",
        required=False,
    )

class IVocabulari3(model.Schema):
    vocabulary_entry = schema.TextLine(
        title=_(u'Vocabulary entries', 'Company Roles'),
        description=u"Each company will be assigned a “Role” during their creation. You need to save this form before continuing",
        required=False,
    )
    

class IVocabulari4(model.Schema):
    location_name = schema.TextLine(
        title=_(u'Vocabulary entries', 'Locations'),
        description=u"Location Name",
        required=False,
    )
    



class IMeetingRows(model.Schema):
    meeting_type = schema.TextLine(
        title=_(u'meeting_type', 'Meeting Type'),
        # description=u"Meeting Type",
        required=False,
    )
    
    meeting_title = schema.TextLine(
        title=_(u'meeting_title', 'Meeting Title'),
        # description=u"Default Meeting Title",
        required=False,
    )
     
    meeting_summary = schema.Text(
        title=_(u'Vmeeting_summary', 'Meeting Tag'),
        # description=u"Default Summary",
        required=False,
    )
    
    # widget(meeting_attendees=SelectWidget)
    # value_type=schema.Choice(vocabulary="plone.app.users.group_ids"),
    # meeting_attendees = schema.List(
    #     title=_("label_attendees_groups", default="Attendees f/group"),
    #     description="",
    #     required=False,
    #     value_type=schema.Choice(vocabulary="plone.app.users.group_ids"),
    # )
    
    
    #  <form:widget type="plone.app.z3cform.widget.AjaxSelectFieldWidget" />
    
    meeting_attendees = schema.Set(
        title=_("label_attendees_groups", default="Attendees groups"),
        description="",
        required=False,
        value_type=schema.Choice(vocabulary="plone.app.users.group_ids"),
    )
    
     
    
    meeting_contact = schema.Choice(
        vocabulary=u"DocentIMS.ActionItems.TeamnamesVocabulary",
        title=_(u"meeting_contact", default=u"Contact Person"),
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
        title=u"Column Titles in Tasks Table.",
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
        title=u"Column Titles in Scope Items Table",
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
        title=_(u"label_company_letter_code", default=u"Company 3-letter code (All Caps)"),
        constraint=company_letter_kodeConstraint,
        )

    # company_role = schema.Text(
    #     required = False,
    #     title=_(u"label_company_role", default=u"Company role")
    #     )
    
    company_role = schema.Choice(
        required = False,
        title=_(u"label_company_role", default=u"Company role"),
        vocabulary=u"DocentIMS.ActionItems.CompanyRolesVocabulary",
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
    company_other_address = schema.Text(
        required = False,
        title=_(u"label_company_other_adress", default=u"Other Address - Optional")
        )

    company_city = schema.TextLine(
        required = False,
        title=_(u"label_company_citye", default=u"City")
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
            'very_short_name',
            'project_description',
            'project_contract_number',
            'project_document_naming_convention',
            'color1',
            'color2',
            'planning_project',
            'template_password',
            'dashboard',
            'dashboard_url'
            ],
        )

    model.fieldset(
        'vocabularies',
        label=_(u'Member Roles'),
        fields=[
            'vokabularies',
            # 'vokabularies2',
        ] 
    )
    
    model.fieldset(
        'locations',
        label=_(u'Locations'),
        fields=[
            'location_names'
        ] 
    )

    model.fieldset(
        'meeting_types',
        label=_(u'Meeting Types'),
        fields=[
            'meeting_types'
        ] 
    )


    model.fieldset(
        'vocabularies3',
        label=_(u'Company Roles'),
        fields=[
            'vokabularies3',
        ] 
    )

    model.fieldset(
        'notifications',
        label=_(u'Due Dates'),
        description=u"Docent IMS color codes certain due dates to aid users in identifying how close an item is to a due date. We use three colors, and you can choose the number of days from the due date each color represents.",
        fields=[
            'future_green',
            'soon_yellow',
            'urgent_red',
            ],
        )
 


    model.fieldset(
        'companies',
        label=_(u'Companies'),
        description=u"Please create all project companies involved in this project.",
        fields=[
            'companies',
            ],
        )

    model.fieldset(
        'table',
        label=_(u'Tasks Table'),
        fields=[
            'table_columns',
            ],
        )
    
    model.fieldset(
        'scope_table',
        label=_(u'Scope Items Table'),
        fields=[
            'scope_table_columns',
            ],
        )

    project_title = schema.TextLine(
        required = True,
        title=_(u"label_title", default=u"Project Full Name"),
        description=_(u"",
                      default=u"")
        )

    #project_full_name = schema.TextLine(
    #    required = False,
    #    title=_(u"label_project_fullname", default=u"Project Full Name"),
    #    description=_(u"help_project_fullname",
    #                  default=u"Project_fullname"),
    #    )

    project_short_name = schema.TextLine(
        title=_(u"label_project_short_name",
        default=u"Project Short Name"),
        description=_(u"",
                      default=u"")
        )
    
    very_short_name = schema.TextLine(
        title=_(u"label_project_very_short_name",
        default=u"Project Very Short Name"),
        description=_(u"",
                      default=u"")
        )
 
    widget(project_description=RichTextFieldWidget)
    project_description = RichTextFieldRegistry(
        title="Project Description",
        required=False,
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
        description=_(u"",
                      default=u"")
        )
 
    
    # widget(project_document_naming_convention=SelectFieldWidget)
    project_document_naming_convention = schema.List(
        title=u"Project Document Naming Convention",
        value_type=schema.Choice(values=[
            u'PrjName',
            u'ContractNumber',
            u'DocState',
            u'Doctype',
            u'DocDate',
            u'DocTime',
        ]),
        required=False,
        default=[],
        missing_value=[],
    )
    
    urgent_red = schema.Int(
        title=_(u"label_red", default=u"Urgent days/value (displayed as Red)"),
        description=" ",
        )
    
    future_green = schema.Int(
        title=_(u"label_green", default=u"Future days/value (displayed as Green)"),
        description="",
        )

    soon_yellow = schema.Int(
        title=_(u"label_yellow", default=u"Soon days/value (displayed as Yellow)"),
        description="",
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
        title = _(u" ",
            default=u""),
        value_type=DictRow(schema=IVocabulari),
        required=True,
    )
    
    widget(vokabularies3=DataGridFieldFactory)
    vokabularies3 = schema.List(
        title = _(u" ",
            default=u""),
        value_type=DictRow(schema=IVocabulari3),
        required=True,
    )
    
    widget(location_names=DataGridFieldFactory)
    location_names = schema.List(
        title = _(u" ",
            default=u""),
        value_type=DictRow(schema=IVocabulari4),
        required=True,
    )
    
    
    widget(meeting_types=DataGridFieldFactory)
    meeting_types = schema.List(
        title = _(u" ",
            default=u""),
        value_type=DictRow(schema=IMeetingRows),
        required=True,
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
            default=u"Select the columns you want to display in the Tasks Table."),
            value_type=DictRow(schema=ITableRows),
    )

    widget(scope_table_columns=DataGridFieldFactory)
    scope_table_columns = schema.List(
        title = _(u"Table Columns",
            default=u"Select the columns you want to display in the Scope Items Table."),
            value_type=DictRow(schema=IScopeTableRows),
    )

    #table_columns = schema.List(
    #    title = _(u"Table Columns",
    #        default=u"Table Column fields"),
    #        value_type=schema.Choice(vocabulary=u"DocentIMS.ActionItems.AiFieldsVocabulary"),
    #)

    # color1 = schema.TextLine(
    #     title=u"Color",
    #     description=u"Choose Color",
    #     required=False,
    #     default="#ff0000"
    # )

    widget(color1=ColorpickerFieldWidget)
    color1 = schema.TextLine(
        title=u"Project Color",
        description=u"",
        # max_length=10,
        required=True,
        default="#ff0000"
    )
    
    widget(color2=ColorpickerFieldWidget)
    color2 = schema.TextLine(
        title=u"Markings Color",
        description=u"",
        # max_length=10,
        required=True,
        default="#ff0000"
    )
    
    planning_project = schema.Bool(
        title=u"Is Planning Project?",
        required=False,
        default=0,
    )
    
    template_password = schema.TextLine(
        title=u"Template Password",
        required=True,
    )
    
    dashboard_url = schema.URI(
        title=u"Url of dashboard",
        required=True,
        default="https://dashboard.docentims.com"
    )    
    
    
    dashboard = schema.TextLine(
        title=u"Dashboard Basic",
        required=True,
    )

alsoProvides(IDocentimsSettings, IMedialogControlpanelSettingsProvider)
