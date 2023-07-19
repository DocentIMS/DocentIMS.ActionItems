# -*- coding: utf-8 -*-

from plone.app.contenttypes.interfaces import IDocument
from plone.dexterity.interfaces import IDexterityContent
from plone.dexterity.interfaces import IDexterityContainer
from plone.indexer import indexer


@indexer(IDexterityContent)
def dummy(obj):
    """ Dummy to prevent indexing other objects thru acquisition """
    raise AttributeError('This field should not indexed here!')


@indexer(IDexterityContainer)  # ADJUST THIS!
def actionIndexer(obj):
    """Calculate and return the value for the indexer"""
    import pdb; pdb.set_trace()
    action_item_no = int(self.id.replace('action-item-', ''))
    obj.action_item_number = action_item_no
    return action_item_no
