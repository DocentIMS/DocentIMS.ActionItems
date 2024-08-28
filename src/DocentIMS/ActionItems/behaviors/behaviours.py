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
        required=False,
        vocabulary= 'DocentIMS.ActionItems.LocationsVocabulary'
    )
    directives.widget("location", AjaxSelectFieldWidget, klass="event_location")

 
@provider(IFormFieldProvider)
class IMeetingContact( IEventContact):
    """Event Contact Schema."""
    
    directives.omitted('contact_email')
    directives.omitted('contact_phone') 

    contact_name = schema.Choice(
        title="Contact Person", 
        required=False,
        vocabulary= 'DocentIMS.ActionItems.FullnamesVocabulary'
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
            vocabulary= 'DocentIMS.ActionItems.FullnamesVocabulary'
            
        )
    )
    directives.widget("attendees",  AjaxSelectFieldWidget, vocabulary= 'DocentIMS.ActionItems.FullnamesVocabulary',  klass="event_attendees")
    
    
    # teste = schema.TextLine(
    #     title="this is a tes",
    #     required=False,
    # )
    # directives.widget("teste",  AjaxSelectWidget, allow_multiple=False, vocabulary= 'DocentIMS.ActionItems.FullnamesVocabulary', )


# @implementer(IEventAttendees)
# @adapter(IMeetingAttendeesMarker)
# class  MeetingAttendees(object):
#     def __init__(self, context):
#         self.context = context

#     @property
#     def attendees(self):
#         import pdb; pdb.set_trace()
#         if safe_hasattr(self.context, 'attendees'):
#             return 'self.context.attendees'
#         return None

#     @attendees.setter
#     def attendees(self, value):
#         self.context.attendees = 'value'