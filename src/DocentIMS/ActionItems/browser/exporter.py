# -*- coding: utf-8 -*-

from Acquisition import aq_inner
from datetime import datetime
#from datetime import timedelta
#from plone.app.contentlisting.interfaces import IContentListingObject
from plone.app.event.base import default_timezone
from plone import api
import csv
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

#from tempfile import TemporaryFile
import io

from icalendar import Calendar
from icalendar import Event
import pytz


try:
	from StringIO import StringIO ## for Python 2
except ImportError:
	from io import StringIO ## for Python 3
 
from io import BytesIO   

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
         
        dato =  self.context.revised_due_date or self.context.initial_due_date
        dt = datetime(dato.year, dato.month, dato.day, 8, 0, 0, 0)
        dt_end = datetime(dato.year, dato.month, dato.day, 18, 0, 0, 0)
        event.add("dtstart", dt)
        event.add("dtend", dt_end)
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


class XActionItemsCSV(BrowserView):
	"""Returns action event in CSV format."""


	def __call__(self):
		# Find all items of content type 'mytype'
		mytype_items = api.content.find(portal_type='action_items')
		
		
		if not mytype_items:
			return "No items of type 'mytype' found."
			#

		# Prepare CSV data
		CSV = []
		#[]= BytesIO()
		for item in mytype_items:
			title = item.Title
			CSV.append(title)
			CSV.append(title)
			
		# Add header
		dataLen = len(CSV)
		R = self.request.RESPONSE
		R.setHeader('Content-Length', dataLen)
		R.setHeader('Content-Type', 'text/csv')
		R.setHeader('Content-Disposition', 'attachment; filename=%s.csv' % self.context.getId())

		#return thefields
		return CSV




class CSVGenericView(BrowserView):
    @property
    def records(self):
        return []

    @property
    def fileprefix(self):
        return "Action_items"

    @property
    def filename(self):
        #return f"{self.fileprefix}-{self.now():%Y-%m-%d %H:%M}.csv"
        return f"{self.fileprefix}-CSV.csv"

    def __call__(self):
        records = self.records
        if not records:
            api.portal.show_message(
                message="No data found for CSV.",
                request=self.request,
                type="error",
            )
            self.request.response.redirect(self.context.absolute_url())
            return "No data."
        self.request.response.setHeader("Content-Type", "text/csv")
        self.request.response.setHeader(
            "Content-Disposition", f"attachment;filename={self.filename}"
        )
        sio = io.StringIO()
        writer = csv.DictWriter(sio, records[0].keys())
        writer.writeheader()
        for record in records:
            writer.writerow(record)
        return sio.getvalue()

class ActionItemsCSV(CSVGenericView):

    @property
    def fileprefix(self):
        return "Some-Data"

    @property
    def records(self):
        result = []
        io.StringIO()
        brains = api.content.find(portal_type='sow_analysis')
        # or action items ?
        for brain in brains:
            obj = brain.getObject()
            # better use an OrderedDict below because in CSV order matters.
            #result.append({"title": obj.Title(), "id": obj.getId()}) # and so on
            result.append({"title": obj.Title(),
                "section number": obj.section_number,
                "assigned to": obj.assigned_to,
                "Closed": obj.is_the_analyis_complete,
            }) # and so on
        return result
