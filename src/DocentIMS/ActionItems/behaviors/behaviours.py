from plone.app.event.dx.behaviors import IEventLocation
from plone.autoform import directives

from plone.app.event.dx.behaviors import IEventLocation, IEventAttendees, IEventContact
from plone.app.z3cform.widget import AjaxSelectFieldWidget
from plone.app.z3cform.widget import AjaxSelectWidget
from zope import schema
from zope.interface import provider
from plone.autoform.interfaces import IFormFieldProvider
# from Products.CMFPlone.utils import safe_hasattr
# from zope.component import adapter
# from zope.interface import Interface
# from zope.interface import implementer

@provider(IFormFieldProvider)
class IMeetingLocation(IEventLocation):
    """Event Location Schema."""

    location = schema.Choice(
        title="Meeting Location",
        description="Location of the meeting",
        required=True,
        vocabulary= 'DocentIMS.ActionItems.LocationsVocabulary'
    )
    directives.widget("location", AjaxSelectFieldWidget, klass="event_location")

 
@provider(IFormFieldProvider)
class IMeetingContact( IEventContact):
    """Event Contact Schema."""
    
    directives.omitted('contact_email')
    directives.omitted('contact_phone') 

    # contact_name = schema.Choice(
    #     title="Contact Person", 
    #     required=False,
    #     vocabulary= 'DocentIMS.ActionItems.FullnamesVocabulary'
    # )
    contact_name = schema.Choice(
        title="Contact Person", 
        required=False,
        vocabulary= 'DocentIMS.ActionItems.TeamnamesVocabulary'
    )
    directives.widget("contact_name", AjaxSelectFieldWidget, klass="event_contact_name")
    
    # @property
    # def contact_phone:
    #     return users phone  
    
# class IMeetingAttendeesMarker(Interface):
#     pass    

@provider(IFormFieldProvider)
# @adapter(IMeetingAttendeesMarker)
class IMeetingAttendees(IEventAttendees):
    """MEETING Attendees Schema."""
    attendees = schema.Tuple(
        title= "Attendees",
        description= "List of attendees.",
        required=False,
        missing_value=(),
        value_type=schema.Choice(
            title="Attendee",
            required=False,
            # vocabulary= 'DocentIMS.ActionItems.FullnamesVocabulary'
            vocabulary= 'DocentIMS.ActionItems.TeamnamesVocabulary'
            
        )
    )
    # directives.widget("attendees",  AjaxSelectFieldWidget, vocabulary= 'DocentIMS.ActionItems.FullnamesVocabulary',  klass="event_attendees")
    directives.widget("attendees",  AjaxSelectFieldWidget, vocabulary= 'DocentIMS.ActionItems.TeamnamesVocabulary',  klass="event_attendees")
    
    