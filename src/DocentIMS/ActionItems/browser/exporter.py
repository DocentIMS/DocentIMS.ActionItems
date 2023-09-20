from Acquisition import aq_inner
from datetime import datetime
#from datetime import timedelta
#from plone.app.contentlisting.interfaces import IContentListingObject
from plone.app.event.base import default_timezone
#from plone.app.event.base import get_events
#from plone.app.event.base import RET_MODE_BRAINS
#from plone.event.interfaces import IEvent
#from plone.event.interfaces import IEventAccessor
#from plone.event.interfaces import IICalendar
#from plone.event.interfaces import IICalendarEventComponent
#from plone.event.interfaces import IOccurrence
from plone.event.utils import is_datetime
from plone.event.utils import tzdel
from plone.event.utils import utc
#from Products.ZCatalog.interfaces import ICatalogBrain
from zope.interface import implementer
from zope.publisher.browser import BrowserView

from icalendar import Calendar
from icalendar import Event
import pytz


PRODID = "-//Plone.org//NONSGML Docent//EN"
VERSION = "2.0"


class ActionItemsICal(BrowserView):
    """Returns action event in iCal format."""

    def get_ical_string(self):
        cal = Calendar()
        cal.add('prodid', PRODID)
        cal.add('version', VERSION)

        event = Event()
        #event.add("dtstamp", utc(datetime.now()))
        event.add("summary", self.context.title)
        event.add("name", self.context.title)
        event.add("description",self.context.Description())
        #import pdb; pdb.set_trace()
        dato =  self.context.revised_due_date or self.context.initial_due_date
        dt = datetime(dato.year, dato.month, dato.day, 8, 0, 0, 0)
        event.add("dtstart", dt)
        #event.add("dtstart", self.context.initial_due_date)
        #change to 8 in the morning
        cal.add_component(event)

        return cal.to_ical()

    def __call__(self):

        ical = self.get_ical_string()
        name = f"{self.context.getId()}.ics"
        self.request.response.setHeader("Content-Type", "text/calendar")
        self.request.response.setHeader(
            "Content-Disposition", f'attachment; filename="{name}"'
        )
        self.request.response.setHeader("Content-Length", len(ical))
        self.request.response.write(ical)
