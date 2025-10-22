from zope.interface import provider, implementer
from zope import schema
# from zope.schema.vocabulary import SimpleVocabulary, SimpleTerm
from plone.autoform.interfaces import IFormFieldProvider
from plone.supermodel import model
from plone.autoform import directives as form
from z3c.form.interfaces import IAddForm
from zope.component import adapter
from zope.interface import Interface 
from zope.interface import provider
from Products.CMFCore.utils import getToolByName
from AccessControl import getSecurityManager
from zope.schema.interfaces import IVocabularyFactory
from zope.interface import provider

from zope.schema.vocabulary import SimpleVocabulary, SimpleTerm


from Products.CMFCore.utils import getToolByName
from zope.interface import provider
from zope.schema.interfaces import IContextSourceBinder
from zope.schema.vocabulary import SimpleVocabulary

@provider(IContextSourceBinder)
def transitionStates(context):
    wf_tool = getToolByName(context, 'portal_workflow')
    request = getattr(context, 'REQUEST', None)

    # Default: no portal_type
    portal_type = None

    if request is not None:
        # Look at the URL to infer type being added
        path_info = request.get('PATH_INFO', '')
        if '++add++' in path_info:
            portal_type = path_info.split('++add++')[-1]
    
    terms = []
    # terms.append(SimpleTerm(value=None, title='Choose'))
    chains = wf_tool.getChainForPortalType(portal_type)
    
    if chains:
            wf = wf_tool[chains[0]]
            initial_state = wf.initial_state

            # Loop through transitions that originate from the initial state
            for t_id in wf.states[initial_state].transitions:
                t = wf.transitions.get(t_id)
                if t:
                    terms.append(SimpleTerm(
                        value=t.id,
                        title=t.new_state_id or t.id
                    ))

    return SimpleVocabulary(terms)

    return SimpleVocabulary(terms)


# Marker interface
class IAutoPublishBehaviorMarker(Interface):    
    pass

@provider(IFormFieldProvider)
class IAutoPublishBehavior(model.Schema):
    """Behavior to auto publish content"""              
    form.mode(transition_target='hidden')
    form.mode(IAddForm, transition_target='input')
    transition_target = schema.Choice(
        title= u"State",
        required= False,
        source=transitionStates,
    )

@implementer(IAutoPublishBehavior)
@adapter(IAutoPublishBehaviorMarker)
class AutoPublishBehavior:
    def __init__(self, context):
        self.context = context 
  
            
