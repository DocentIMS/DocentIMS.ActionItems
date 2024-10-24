# -*- coding: utf-8 -*-

from plone import api
# from plone.app.textfield import RichText
# from zope.i18nmessageid import MessageFactory
import transaction
# from zope.interface import alsoProvides
# from zope.interface import directlyProvides
from zope.interface import Interface
from zope.lifecycleevent import IObjectModifiedEvent
from zope.lifecycleevent import IObjectModifiedEvent

# from zope.lifecycleevent import IObjectAddedEvent"
#from zope.schema.interfaces import IContextSourceBinder
# from zope.schema.interfaces import  InvalidValue
# from AccessControl import Unauthorized
from Products.statusmessages.interfaces import IStatusMessage
from datetime import datetime

# import transaction
# from zope.container.contained import notifyContainerModified
# from zope.event import notify

from zExceptions import Redirect
from zope.component import getMultiAdapter
        


def check_defaultpage(object, event):
    #Dont delete default page
    try:
        membership_tool = object.portal_membership

        # Get the current authenticated user
        current_user = membership_tool.getAuthenticatedMember()
        roles = current_user.getRoles()
        if 'Manager' in roles:
                # OK to delete since Manager should know what he/she is doing
                pass

        else:
                if hasattr(object, 'aq_parent') and object.aq_inner.aq_parent.id not in ['events', 'news']:
                    if hasattr(object.aq_inner.aq_parent, 'default_page') and  object.aq_inner.aq_parent.default_page  == object.id:
                        if not '@@fc-delete'  in object.REQUEST.getURL():
                            messages = IStatusMessage(object.REQUEST)
                            messages.addStatusMessage(u"You can not delete the default view of a folder.", type="error")
                        raise Redirect(object.absolute_url())
                # pass
                
    except AttributeError:
        pass        
    
def add_meeting_types(object, event):
    today = datetime.today().strftime('%Y-%m-%d')
    if object.portal_type in  ['Meeting', 'meeting' ]:
        context = object
        parent_id = context.UID()
        meeting_date_time = context.start.date()
        location = context.location
        
        portal_types = api.portal.get_tool('portal_types')

        # List all content types
        content_types = portal_types.objectIds()
        
        if 'meeting_agenda' in content_types:
            agenda_content = api.content.create(
                            type='meeting_agenda',
                            container=context,
                            parent_id=parent_id,
                            title=f"Agenda {meeting_date_time}",
                            id=f"agenda-{parent_id}",
        )
            
        if 'Meeting Agenda' in content_types:
            agenda_content = api.content.create(
                            type='Meeting Agenda',
                            container=context,
                            parent_id=parent_id,
                            title=f"Agenda {meeting_date_time}",
                            id=f"agenda-{parent_id}",
        )
            
        if 'meeting_notes' in content_types:
            notes = api.content.create(
                            type='meeting_notes',
                            container=context,
                            parent_id=parent_id,
                            meeting_date_time=meeting_date_time,
                            title=f"Notes {meeting_date_time}",
                            meeting_location=location,
                            description="Notes taken during the meeting",
                            id=f"note-{parent_id}",
            )
            
        if 'Meeting Notes' in content_types:
            notes = api.content.create(
                            type='Meeting Notes',
                            container=context,
                            parent_id=parent_id,
                            meeting_date_time=meeting_date_time,
                            title=f"Notes {meeting_date_time}",
                            meeting_location=location,
                            description="Notes taken during the meeting",
                            id=f"notes-{parent_id}",
            )
        
        if 'meeting_minutes' in content_types:
            minutes = api.content.create(
                            type='meeting_minutes',
                            container=context,
                            parent_id=parent_id,
                            title=f"Minutes {meeting_date_time}",
                            id=f"minute-{parent_id}",                  
            )
        
        
        
        
        if 'Meeting Minutes' in content_types:
            minutes = api.content.create(
                            type='Meeting Minutes',
                            container=context,
                            parent_id=parent_id,
                            title=f"Minutes {today}",
                            id=f"minute-{parent_id}",                  
            )
        
       

        
def change_uuid(object, event):
    if object.portal_type in  ['action_items' ]:
        #import pdb; pdb.set_trace()
        if hasattr(object, 'placeholder'):
            if object.placeholder is not None:
                lenght = len( object.placeholder ) 
                if  lenght == 32:
                    setattr(object, '_plone.uuid', object.placeholder) 
                    #setattr(object, 'related_sow_section', object.placeholder) 
                    setattr(object, 'placeholder', '') 
                    transaction.commit()
                    
def remove_description(object, event):
    if object.portal_type in  ['action_items', 'sow_analysis' ]:
        if hasattr(object, 'Description'):
            a=1
            # object.setDescription('')

def change_title(object, event):  
    if object.portal_type in  ['postit_note', 'PostIt Note' ]:
        if hasattr(object, 'Description'):
            description = object.Description().split()
            tittel =  ' '.join(description[:5])
            setattr(object, 'title', tittel) 
            transaction.commit()
        
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
                

        