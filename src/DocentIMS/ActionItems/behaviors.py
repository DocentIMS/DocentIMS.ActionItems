from plone.app.event.dx.behaviors import IEventLocation
from plone.autoform import directives

from plone.app.event.dx.behaviors import IEventLocation, IEventAttendees, IEventContact
from plone.app.z3cform.widget import AjaxSelectFieldWidget
from zope import schema
from zope.interface import provider
from plone.autoform.interfaces import IFormFieldProvider

@provider(IFormFieldProvider)
class IMeetingLocation(IEventLocation):
    """Event Location Schema."""

    location = schema.Choice(
        title="Meeting Location",
        description="Location of the meeting",
        required=False,
        vocabulary= 'DocentIMS.ActionItems.LocationsVocabulary'
    )
    directives.widget("location", AjaxSelectFieldWidget, klass="event_location")

 
@provider(IFormFieldProvider)
class IMeetingContact( IEventContact):
    """Event Contact Schema."""

    contact_name = schema.Choice(
        title="Contact Person", 
        required=False,
        vocabulary= 'DocentIMS.ActionItems.FullnamesVocabulary'
    )
    directives.widget("contact_name", AjaxSelectFieldWidget, klass="event_contact_name")


@provider(IFormFieldProvider)
class IMeetingAttendees(IEventAttendees):
    """MEETING Attendees Schema."""

    attendees = schema.List(
        title= "Attendees",
        description= "List of attendees.",
        value_type=schema.Choice(
            title="Attendee",
            required=False,
            vocabulary=  'DocentIMS.ActionItems.FullnamesVocabulary'
            
        )
    )
    directives.widget("attendees",  AjaxSelectFieldWidget, vocabulary= 'DocentIMS.ActionItems.FullnamesVocabulary',  klass="event_attendees")