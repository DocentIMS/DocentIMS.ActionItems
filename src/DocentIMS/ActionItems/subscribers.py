# -*- coding: utf-8 -*-

from plone import api
from plone.app.textfield import RichText
from zope.i18nmessageid import MessageFactory
import transaction
# from zope.interface import alsoProvides
# from zope.interface import directlyProvides
from zope.interface import Interface
from zope.lifecycleevent import IObjectModifiedEvent
# from zope.lifecycleevent import IObjectAddedEvent"

#from zope.schema.interfaces import IContextSourceBinder


def change_uuid(object, event):
    if object.portal_type in  ['action_items' ]:
        #import pdb; pdb.set_trace()
        if hasattr(object, 'placeholder'):
            if object.placeholder is not None:
                lenght = len( object.placeholder ) 
                if  lenght == 32:
                    setattr(object, '_plone.uuid', object.placeholder) 
                    setattr(object, 'placeholder', '') 
                    transaction.commit()
                    
def remove_description(object, event):
    if object.portal_type in  ['action_items', 'sow_analysis' ]:
        if hasattr(object, 'Description'):
            a=1
            # object.setDescription('')
        
def last_state(object, event):
    #subscribers.last_state
    #histo = event.transition.variables.review_history
    #event.transition.variables.__dict__
    #event.transition.variables.review_history.__dict__
    #event.transition.variables.review_history.__doc__
    #__name__ 
    
    if event.transition.__name__ == 'last_state':
        try:
            api.content.transition(obj=object, transition=object.formertransitiontwo)
        #except  InvalidParameterError: 
        #    #Add some message 
        #    a = 1
        finally:
             a= 1
             api.portal.show_message(message='Action / Item Change  Not Allowed',type='warning')
        #     #Add some message 
            
        #return
        # .__name__ == 'last_state':
       
    else:
        #Store state so one can revert
        object.formertransitiontwo =  object.formertransition or None
        object.formertransition = event.transition.__name__
    
    

def save_note(object, event):
    """Make notes content items"""
    if object.portal_type == 'action_items':
        context = object
        user =  api.user.get_current().getMemberId()
        item = api.content.find(context=context, id=user, portal_type='personal_notes' )
        
        # if object.portal_type in  ['action_items', 'sow_analysis' ]:
        #     if hasattr(object, 'Description'):
        #         a=1
            
            
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
                

        