from zope.interface import directlyProvides
from zope.schema.vocabulary import SimpleVocabulary, SimpleTerm
from zope.schema.interfaces import IVocabularyFactory
from plone import api

#from zope.i18nmessageid import MessageFactory
#_ = MessageFactory('DocentIMS.ActionItems')

def format_title(folder):
    return "{}  ...   [ {} ]".format( folder.Title, folder.getURL())


def ShowActionItemsVocabulary(context):
    items = api.content.find(portal_type=['sow_analysis', 'SOW Analysis'], sort_on='sortable_title')
    if items:
        terms = [ SimpleTerm(value=item.UID, token=item.UID, title=item.Title) for item in items ]
    return SimpleVocabulary(terms)

directlyProvides(ShowActionItemsVocabulary, IVocabularyFactory)


def ActionItemsVocabulary(context):
    items = api.content.find(portal_type=['action_items', 'action_item'], sort_on='sortable_title')
    if items:
        terms = [ SimpleTerm(value=item.UID, token=item.UID, title=item.Title) for item in items ]
    return SimpleVocabulary(terms)

directlyProvides(ActionItemsVocabulary, IVocabularyFactory)
