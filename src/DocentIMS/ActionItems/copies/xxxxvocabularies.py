from zope.interface import directlyProvides
from zope.schema.vocabulary import SimpleVocabulary, SimpleTerm
from zope.schema.interfaces import IVocabularyFactory
from plone import api

from .interfaces import IDocentimsSettings

#from zope.i18nmessageid import MessageFactory
#_ = MessageFactory('DocentIMS.ActionItems')

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
    items = api.content.find(portal_type=['Company', 'company', 'project_company', 'project_companies'], sort_on='sortable_title')
    if items:
        terms = [ SimpleTerm(value=item.UID, token=item.UID, title=item.Title) for item in items ]
        return SimpleVocabulary(terms)
    return SimpleVocabulary([])

directlyProvides(CompanyVocabulary, IVocabularyFactory)



def SiteVocabulary(context):
    items  =  api.portal.get_registry_record('vokabulary', interface=IDocentimsSettings)
    if items:
        terms = [ SimpleTerm(value=item, token=item.lower(), title=item) for item in items ]
        return SimpleVocabulary(terms)
    return SimpleVocabulary([])

directlyProvides(SiteVocabulary, IVocabularyFactory)


def PriorityVocabulary(context):

    return SimpleVocabulary(
        [SimpleTerm(value=1, title=_(u'1 Critical')),
         SimpleTerm(value=2, title=_(u'2 Medium')),
         SimpleTerm(value=3, title=_(u'3 Low'))]
        )

directlyProvides(PriorityVocabulary, IVocabularyFactory)
