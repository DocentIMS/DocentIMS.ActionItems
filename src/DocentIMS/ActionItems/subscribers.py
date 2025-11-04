# -*- coding: utf-8 -*-

# from plone.app.textfield import RichText
# from zope.i18nmessageid import MessageFactory
# from zope.interface import alsoProvides
# from zope.interface import directlyProvides

from plone import api
from plone import api
from plone.api import content
from plone.api.exc import InvalidParameterError
# from Products.PluggableAuthService.events import PropertiesUpdated
from Products.statusmessages.interfaces import IStatusMessage
from zExceptions import Redirect
from zope.component import adapter
from zope.component import getMultiAdapter
from zope.interface import Interface
from zope.lifecycleevent import IObjectModifiedEvent
from zope.lifecycleevent.interfaces import IObjectAddedEvent
import base64
import json
import random
import requests
import string
import transaction
from datetime import datetime
from DocentIMS.ActionItems.behaviors.auto_publish_behavior import IAutoPublishBehavior
from DocentIMS.ActionItems.interfaces import IDocentimsSettings


@adapter(IAutoPublishBehavior, IObjectAddedEvent)
def auto_publish_on_add(obj, event):
    # Ensure we don't do this during copy/paste or move
    if not event.object == obj:
        return
    
     
    transition = obj.transition_target
    
    # Only do this if the object is not already published
    if transition:
        if not api.content.get_state(obj) == transition:
            try:
                api.content.transition(obj=obj, transition=transition)
            except Exception as e:
                # Log error if needed
                pass
            # finally:
            #     pass


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
        object.setSubject((object.meeting_type,))  # Set tags; it takes a tuple or a list of strings
        object.reindexObject(idxs=['Subject']) 
        
        portal_types = api.portal.get_tool('portal_types')

        # List all content types
        content_types = portal_types.objectIds()
        
        if 'meeting_agenda' in content_types:
            agenda_content = api.content.create(
                            type='meeting_agenda',
                            container=context,
                            parent_id=parent_id,
                            title=f"Agenda {meeting_date_time}",
                            id=f"agenda",
        )
            
        if 'Meeting Agenda' in content_types:
            agenda_content = api.content.create(
                            type='Meeting Agenda',
                            container=context,
                            parent_id=parent_id,
                            title=f"Agenda {meeting_date_time}",
                            id=f"agenda",
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
                            id=f"notes",
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
                            id=f"notes",
            )
        
        if 'meeting_minutes' in content_types:
            minutes = api.content.create(
                            type='meeting_minutes',
                            container=context,
                            parent_id=parent_id,
                            title=f"Minutes {meeting_date_time}",
                            id=f"minutes",                  
            )
        
        
        
        
        if 'Meeting Minutes' in content_types:
            minutes = api.content.create(
                            type='Meeting Minutes',
                            container=context,
                            parent_id=parent_id,
                            title=f"Minutes {today}",
                            id=f"minutes",                  
            )
        
       

        
def change_uuid(object, event):
    if object.portal_type in  ['action_items' ]:
         
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
    



def close_task(object, event):
    """Go to Closed State based on"""
    if object.portal_type == 'action_items':
        # context = object
        if api.content.get_state(object) != 'Closed':
            #Go to Closed state
            if object.is_this_item_closed: 
                try:
                    api.content.transition(obj=object, transition='close')
                    api.portal.show_message(message='Moved to Closed State', type='info')
                except InvalidParameterError: 
                    api.portal.show_message(message='Could not move to Closed state. Workflow does not allow or was already Closed',type='error')
            else: 
                pass               
                # api.portal.show_message(message='This Task was already Closed',type='warning')
            


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
                

def user_created_handler(event):
    """Handles a new user creation."""
    try:
            dashboard_url = api.portal.get_registry_record('dashboard_url', interface=IDocentimsSettings) or 'https://dashboard.docentims.com'
            site_url = dashboard_url + "/++api++/@users"
            user = event.object
            email  = user.getProperty('email', None)
            
            # Create a new user on dashboard site
            if email:
                basik =  api.portal.get_registry_record('dashboard', interface=IDocentimsSettings) or ''
                username = user.getUserName()
                fullname = user.getProperty('fullname')
                if fullname:
                    password = ''.join(random.choices(string.ascii_letters, k=27))     
                    
                    added_user = requests.post(
                            site_url,
                            headers={
                                'Content-Type': 'application/json',
                                'Authorization': f'Basic {basik}'
                            },
                            data = json.dumps({
                                'email': email,
                                'password': password,
                                'fullname': fullname,
                                'roles': ['Member'] 
                            })
                        )
                    
                    import pdb; pdb.set_trace()
                    if added_user.status_code == 200 or added_user.status_code == 201:
                        api.portal.show_message(message='User was added to Dashboard site',type='info')    
                    elif added_user.status_code != 500 or added_user.status_code != 501:
                        # User probabaly exists already
                        # Maybe we want to update info                        
                        api.portal.show_message(message='User was not added/updated to Dashboard Site. Check password in control panel', type='error')                         
                    else:
                        # Do nothing, probably
                        ok = 1
                        # api.portal.show_message(message='User was not added to Dashboard Site. Check password in control panel', type='error')
                        
    except KeyError:
            api.portal.show_message(message='User was not added to Dashboard Site. Check password in control panel.',type='warning')
            pass   
        
    except requests.exceptions.SSLError:
            api.portal.show_message(message='User was not added to Dashboard Site. SSH Certificate on Docent needs revival',type='error')
        
    #     return True
    
    # return False
        