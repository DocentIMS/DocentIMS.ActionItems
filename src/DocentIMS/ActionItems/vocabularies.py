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
    #import pdb; pdb.set_trace()
    #TO DO: Maybe check if they are unique
    if items:
        terms = [ SimpleTerm(value=item['short_company_name'], token=item['short_company_name'], title=item['short_company_name']) for item in items ]
        return SimpleVocabulary(terms)
    return SimpleVocabulary([])

directlyProvides(CompanyVocabulary, IVocabularyFactory)


#def SiteVocabulary(context):
#    items  =  api.portal.get_registry_record('vokabulary', interface=IDocentimsSettings)
#    if items:
#        terms = [ SimpleTerm(value=item, token=item.lower(), title=item) for item in items ]
#        return SimpleVocabulary(terms)
#    return SimpleVocabulary([])
#
#directlyProvides(SiteVocabulary, IVocabularyFactory)

def ProjectRolesVocabulary(context):
    items  =  api.portal.get_registry_record('vokabularies', interface=IDocentimsSettings)

    if items:
        entries = set([ item['vocabulary_entry'] for item in items ])
        terms = [ SimpleTerm(value=item, token=item.lower(), title=item) for item in entries]
        return SimpleVocabulary(terms)
    return SimpleVocabulary([])

directlyProvides(ProjectRolesVocabulary, IVocabularyFactory)


def Site2Vocabulary(context):
    items  =  api.portal.get_registry_record('vokabularies2', interface=IDocentimsSettings)

    if items:
        entries = set([ item['vocabulary_entry'] for item in items ])
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

def AiFieldsVocabulary(context):
    return SimpleVocabulary(
        [
            SimpleTerm(value='actionno', token='actionno', title=_(u'actionno')),
            SimpleTerm(value='title', token='title', title=_(u'Title')),
            SimpleTerm(value='description', token='description', title=_(u'Description')),
            SimpleTerm(value='priority', token='priority', title=_(u'Priority')),
            SimpleTerm(value='assigned_to', token='assigned_to', title=_(u'Assigned To')),
            SimpleTerm(value='related_item', token='related_item', title=_(u'Related')),
            SimpleTerm(value='Creator', token='Creator', title=_(u'Creator')),
            SimpleTerm(value='initial_due_date', token='initial_due_date', title=_(u'iIni Due Date')),
            SimpleTerm(value='duedate', token='duedate', title=_(u'Due Date')),
            SimpleTerm(value='modified', token='modified', title=_(u'modified')),
            SimpleTerm(value='revised_due_date', token='revised_due_date', title=_(u'Rev Due Date')),
            SimpleTerm(value='is_this_action_out_of_the_scope_of_work_', token='is_this_action_out_of_the_scope_of_work_', title=_(u'Out of Scope')),
            SimpleTerm(value='related_sow_section', token='related_sow_section', title=_(u'Rel Scope')),
            SimpleTerm(value='is_this_item_closed', token='is_this_item_closed', title=_(u'Closed?')),
        ]
    )

directlyProvides(AiFieldsVocabulary, IVocabularyFactory)
