# -*- coding: utf-8 -*-

from plone import api
from plone.app.textfield import RichText
from zope.i18nmessageid import MessageFactory
# from zope.interface import alsoProvides
# from zope.interface import directlyProvides
from zope.interface import Interface
from zope.lifecycleevent import IObjectModifiedEvent
#from zope.schema.interfaces import IContextSourceBinder

def last_state(object, event):
    #subscribers.last_state
    histo = event.transition.variables.review_history
    import pdb; pdb.set_trace()
    if event.transition.__name__ == 'last_state':
        #something here
        import pdb; pdb.set_trace()
    

def save_note(object, event):
    """Make notes content items"""
    if object.portal_type == 'action_items':
        context = object
        user =  api.user.get_current().getMemberId()
        item = api.content.find(context=context, id=user, portal_type='personal_notes' )
            
            
        #Update personal note with content
        if  IObjectModifiedEvent.providedBy(event):
            #import pdb; pdb.set_trace()
            if not item:
                # not object.private_notes = None
                if object.private_notes:
                    item = api.content.create(
                        type='personal_notes',
                        container=context,
                        id=user,
                        title=user, 
                        bodytext=object.private_notes
                    )
                    
            
            else:
                notes_item = item[0].getObject()
                notes_item.bodytext = object.private_notes
                object.private_notes = None
                
                #item[0].getObject().bodytext
                

        