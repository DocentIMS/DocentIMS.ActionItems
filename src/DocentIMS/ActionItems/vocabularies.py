from zope.interface import directlyProvides
from zope.schema.vocabulary import SimpleVocabulary, SimpleTerm
from zope.schema.interfaces import IVocabularyFactory
from plone import api


from .interfaces import IDocentimsSettings

from zope.i18nmessageid import MessageFactory
_ = MessageFactory('DocentIMS.ActionItems')

def format_title(folder):
    return "{}  ...   [ {} ]".format( folder.Title, folder.getURL())


def ShowActionItemsVocabulary(context):
    items = api.content.find(portal_type=['sow_analysis', 'SOW Analysis'], sort_on='sortable_title')
    if items:
        terms = [ SimpleTerm(value=item.UID, token=item.UID, title=item.Title) for item in items ]
        return SimpleVocabulary(terms)
    return SimpleVocabulary([])

directlyProvides(ShowActionItemsVocabulary, IVocabularyFactory)


def ActionItemsVocabulary(context):
    items = api.content.find(portal_type=['action_items', 'action_item', 'Action Items'], sort_on='sortable_title')
    if items:
        terms = [ SimpleTerm(value=item.UID, token=item.UID, title=item.Title) for item in items ]
        return SimpleVocabulary(terms)
    return SimpleVocabulary([])

directlyProvides(ActionItemsVocabulary, IVocabularyFactory)


def CompanyVocabulary(context):
    items  =  api.portal.get_registry_record('companies', interface=IDocentimsSettings)
    if items:
        # Assuming items is a list of dictionaries

        # Use sorted() to create a sorted list of items based on 'short_company_name'
        #sorted_items = sorted(items, key=lambda x: x['short_company_name'])
        sorted_items = sorted(
            filter(lambda x: x.get('short_company_name', '') is not None, items),
            key=lambda x: x.get('short_company_name', '').lower() if x.get('short_company_name') else ''
        )

        # Create SimpleTerm objects from the sorted list, excluding empty 'short_company_name'
        terms = [
            SimpleTerm(value=item['short_company_name'], token=item['short_company_name'], title=item['short_company_name'])
            for item in sorted_items if item['short_company_name'] and len(item['short_company_name']) > 1
        ]
        return SimpleVocabulary(terms)
    
    return SimpleVocabulary([])

directlyProvides(CompanyVocabulary, IVocabularyFactory)


def LocationsVocabulary(context):
    items  =  api.portal.get_registry_record('location_names', interface=IDocentimsSettings)
    if items:
        # Assuming items is a list of dictionaries

        sorted_items = sorted(
            filter(lambda x: x.get('location_name', '') is not None, items),
            key=lambda x: x.get('location_name', '').lower() if x.get('location_name') else ''
        )

        # Create SimpleTerm objects from the sorted list, excluding empty 'location_names'
        terms = [
            SimpleTerm(value=item['location_name'], token=item['location_name'], title=item['location_name'])
            for item in sorted_items if item['location_name'] and len(item['location_name']) > 1
        ]
        return SimpleVocabulary(terms)
    
    return SimpleVocabulary([])

directlyProvides(LocationsVocabulary, IVocabularyFactory)



#def SiteVocabulary(context):
#    items  =  api.portal.get_registry_record('vokabulary', interface=IDocentimsSettings)
#    if items:
#        terms = [ SimpleTerm(value=item, token=item.lower(), title=item) for item in items ]
#        return SimpleVocabulary(terms)
#    return SimpleVocabulary([])
#
#directlyProvides(SiteVocabulary, IVocabularyFactory)

def ProjectRolesVocabulary(context):
    items = api.portal.get_registry_record('vokabularies', interface=IDocentimsSettings)
    
    #   import pdb; pdb.set_trace()

    if items:
        # Extract unique entries from items and convert to lowercase for case-insensitive comparison
        
        # Create SimpleTerm objects from the unique entries
        terms = [
            SimpleTerm(value=item['vocabulary_entry'], token=item['vocabulary_entry'].lower(), title=item['vocabulary_entry'])
            for item in sorted(items, key=lambda x: x.get('vocabulary_entry', '').lower())
            if item.get('vocabulary_entry')  # Exclude items with None or empty 'short_company_name'
        ]

        return SimpleVocabulary(terms)

    return SimpleVocabulary([])

directlyProvides(ProjectRolesVocabulary, IVocabularyFactory)


def Site2Vocabulary(context):
    all_items  =  api.portal.get_registry_record('vokabularies2', interface=IDocentimsSettings)
    set_items = set(all_items)

    if set_items:
        items = list(set_items)
        entries = set([ item['vocabulary_entry'] for item in items.sort() ])
        terms = [ SimpleTerm(value=item, token=item.lower(), title=item) for item in entries]
        return SimpleVocabulary(terms)
    return SimpleVocabulary([])

directlyProvides(Site2Vocabulary, IVocabularyFactory)

# def PriorityVocabulary(context):
#     red  =  api.portal.get_registry_record('red', interface=IDocentimsSettings)
#     yellow  =  api.portal.get_registry_record('yellow', interface=IDocentimsSettings)
#     green  =  api.portal.get_registry_record('green', interface=IDocentimsSettings)

#     return SimpleVocabulary(
#         [SimpleTerm(value=red, token=red, title=_(u'1 Red Critical')),
#          SimpleTerm(value=yellow, token=yellow, title=_(u'2 Yellow Medium')),
#          SimpleTerm(value=green, token=green, title=_(u'3 Green Low'))]
#         )
#     return SimpleVocabulary([])

# directlyProvides(PriorityVocabulary, IVocabularyFactory)

def PriorityVocabulary(context):

    return SimpleVocabulary(
        [SimpleTerm(value=1, token=1, title=_(u'1 Important')),
         SimpleTerm(value=2, token=2, title=_(u'2 Medium')),
         SimpleTerm(value=3, token=3, title=_(u'3 Low'))]
        )
directlyProvides(PriorityVocabulary, IVocabularyFactory)


def QPVocabulary(context):

    return SimpleVocabulary(
        [ 
            SimpleTerm(value='OS',  token='OS',  title=_(u'OS')),
            SimpleTerm(value='DD',  token='DD',  title=_(u'DD')),
            SimpleTerm(value='DQC', token='DQC', title=_(u'DQC')),
            SimpleTerm(value='QA',  token='QA',  title=_(u'QA')),
            SimpleTerm(value='N/A', token='N/A', title=_(u'N/A')),
            SimpleTerm(value='VC',  token='VC',  title=_(u'VC')),
        ]

    )

directlyProvides(QPVocabulary, IVocabularyFactory)



def AiFieldsVocabulary(context):
    return SimpleVocabulary(
        [
            SimpleTerm(value='actionno', token='actionno', title=_(u'AI Number')),
            SimpleTerm(value='title', token='title', title=_(u'Title')),
            SimpleTerm(value='priority', token='priority', title=_(u'Priority')),
            SimpleTerm(value='assigned_to', token='assigned_to', title=_(u' Responsible')),
            SimpleTerm(value='Creator', token='Creator', title=_(u'Creator')),
            SimpleTerm(value='initial_due_date', token='initial_due_date', title=_(u'Initial Due Date')),
            SimpleTerm(value='duedate', token='duedate', title=_(u'Due Date')),
            SimpleTerm(value='modified', token='modified', title=_(u'Date Modified')),
            SimpleTerm(value='is_this_action_out_of_the_scope_of_work_', token='is_this_action_out_of_the_scope_of_work_', title=_(u'Out of Scope')),
            SimpleTerm(value='related_sow_section', token='related_sow_section', title=_(u'Rel Scope Number')),
            SimpleTerm(value='is_this_item_closed', token='is_this_item_closed', title=_(u'Closed?')),
            SimpleTerm(value='daysleft', token='daysleft', title=_(u'Workdays Left')),
        ]
    )
    

directlyProvides(AiFieldsVocabulary, IVocabularyFactory)


def SowFieldsVocabulary(context):
    return SimpleVocabulary(
        [
            #SimpleTerm(value='action_items_related_will_be_listed_here', token='action_items_related_will_be_listed_here', title=_(u'action_items_related_will_be_listed_here')),
            SimpleTerm(value='section_number', token='section_number', title=_(u'Breakdown Number')),
            SimpleTerm(value='title', token='title', title=_(u'Title')),
            SimpleTerm(value='initial_due_date', token='initial_due_date', title=_(u'Initial Due Date')),
            SimpleTerm(value='duedate', token='duedate', title=_(u'Due Date')),
            SimpleTerm(value='estimated_qc_time', token='estimated_qc_time', title=_(u'Estimated QC Time')),
            SimpleTerm(value='internal_qc_required_', token='internal_qc_required_', title=_(u'Internal QC Required')),
            SimpleTerm(value='is_the_analyis_complete', token='is_the_analyis_complete', title=_(u'Closed')),
            SimpleTerm(value='daysleft', token='daysleft', title=_(u'Workdays Left')),
            SimpleTerm(value='assigned_to', token='assigned_to', title=_(u'Responsible')),
            SimpleTerm(value='modified', token='modified', title=_(u'Date Modified')),
            SimpleTerm(value='target_relations', token='target_relations', title=_(u'Rel Action Item')),
        ]
    )

directlyProvides(SowFieldsVocabulary, IVocabularyFactory)



# def CompanyRolesVocabulary(context):
#     return SimpleVocabulary(
#         [
#             SimpleTerm(value='prime', token='prime', title=_(u'Prime')),
#             SimpleTerm(value='architect', token='architect', title=_(u'Architect')),
#             SimpleTerm(value='geotechnical', token='geotechnical', title=_(u'Geotechnical')),
#             SimpleTerm(value='outreach', token='outreach', title=_(u'Outreach')),
#         ]
#     )

# directlyProvides(CompanyRolesVocabulary, IVocabularyFactory)



def CompanyRolesVocabulary(context):
    items = api.portal.get_registry_record('vokabularies3', interface=IDocentimsSettings)
    
    #   import pdb; pdb.set_trace()

    if items:
        # Extract unique entries from items and convert to lowercase for case-insensitive comparison
        
        # Create SimpleTerm objects from the unique entries
        terms = [
            SimpleTerm(value=item['vocabulary_entry'], token=item['vocabulary_entry'].lower(), title=item['vocabulary_entry'])
            for item in sorted(items, key=lambda x: x.get('vocabulary_entry', '').lower())
            if item.get('vocabulary_entry')  # Exclude items with None or empty 'short_company_name'
        ]

        return SimpleVocabulary(terms)

    return SimpleVocabulary([])

directlyProvides(CompanyRolesVocabulary, IVocabularyFactory)


#Assigned to / 
#SimpleTerm(value='id', token='id', title=_(u'id')),
            