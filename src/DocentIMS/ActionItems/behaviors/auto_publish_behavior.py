from zope.interface import provider, implementer
from zope import schema
# from zope.schema.vocabulary import SimpleVocabulary, SimpleTerm
from plone.autoform.interfaces import IFormFieldProvider
from plone.supermodel import model
from plone.autoform import directives as form
from z3c.form.interfaces import IAddForm
# from Products.CMFCore.utils import getToolByName
from zope.component import adapter
from zope.interface import Interface
# Register the vocabulary function
# from zope.schema.vocabulary import VocabularyRegistry

# from zope.schema.interfaces import IVocabularyFactory
from zope.interface import implementer


# Marker interface
class IAutoPublishBehaviorMarker(Interface):
    pass

@provider(IFormFieldProvider)
class IAutoPublishBehavior(model.Schema):
    """Behavior to auto publish content"""

    form.mode(transition_state='hidden')
    form.mode(IAddForm, transition_state='input')
    transition_state = schema.Choice(
        title=u"State",
        required=False,
        vocabulary="DocentIMS.ActionItems.TransitionVocabulary"
    )

@implementer(IAutoPublishBehavior)
@adapter(IAutoPublishBehaviorMarker)
class AutoPublishBehavior:
    def __init__(self, context):
        self.context = context

