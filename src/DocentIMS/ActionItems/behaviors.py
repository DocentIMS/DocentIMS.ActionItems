from plone.app.event.dx.behaviors import IEventLocation
from plone.autoform import directives

from plone.app.event.dx.behaviors import IEventLocation
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

 
