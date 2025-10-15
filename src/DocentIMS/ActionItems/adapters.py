# -*- coding: utf-8 -*-

from zope.interface import Interface
from zope.component import adapter
from plone.stringinterp.adapters import BaseSubstitution
from plone import api

from DocentIMS.ActionItems.interfaces import IDocentimsSettings


@adapter(Interface)
class AssignedTo(BaseSubstitution):
    category = "Users"
    description = "Assigned To"

    def safe_call(self):
      if hasattr(self.context, 'assigned_to'):
        return self.context.assigned_to
      return ''

class DaysLeft(BaseSubstitution):
    category = "All Content"
    description = "Days left"

    def safe_call(self):
      if hasattr(self.context, 'daysleft'):
        return self.context.daysleft
      return ''

class DateChanged(BaseSubstitution):
    category = "All Content"
    description = "Date Changed"

    def safe_call(self):
      if hasattr(self.context, 'start'):
        start = self.context.start
        if hasattr(self.context, 'oldstart'):
            if self.context.oldstart != start:
                return """IMPORTANT: new date
                {}""".format( start.strftime('%Y-%m-%d %H:%M:%S') )
        self.context.oldstart = start
      return ''

@adapter(Interface)
class AssignedMail(BaseSubstitution):
    category = "Users"
    description = "Assigned To Email"
    def safe_call(self):
      if hasattr(self.context, 'assigned_to'):
        #return assigned users email
        return api.user.get(userid=self.context.assigned_to).getProperty('email')
      
      return 'dummyuser@docentims.com'


@adapter(Interface)
class Attendees(BaseSubstitution):
    category = "Users"
    description = "Attendees"

    def safe_call(self):
      if hasattr(self.context, 'attendees'):
        #return attendees users email
        emaillist = []
        attendees = self.context.attendees 
        for attendee in self.context.attendees:
            emaillist.append(api.user.get(userid=attendee).getProperty('email')) or None
        return  ', '.join(emaillist)
        
        #return self.context.attendees 
      
      return 'dummyuser@docentims.com'



@adapter(Interface)
class AssignedFullName(BaseSubstitution):
    category = "Users"
    description = "Assigned To Fullname"

    def safe_call(self):
      if hasattr(self.context, 'assigned_to'):
        #return assigned users email
        return api.user.get(userid=self.context.assigned_to).getProperty('fullname')
      
      return ''


@adapter(Interface)
class ProjectShortName(BaseSubstitution):
    category = "All Content"
    description = "Project Short Name "

    def safe_call(self):
      return  api.portal.get_registry_record('project_short_name', interface=IDocentimsSettings) or ''


        
# @adapter(Interface)
# class DueDate(BaseSubstitution):
#     category = "All Content"
#     description = "Due Date"

#     def safe_call(self):
#        
#       if hasattr(self.context, 'initial_due_date'):
#         return self.context.revised_due_date or self.context.initial_due_date
#       return ''       
        

# // Not an adapter, move it to another file later
# TO DO 
# from io import BytesIO
# from Products.PortalTransforms.interfaces import ITransform
# from zope.interface import implementer

# import docx2txt


# @implementer(ITransform)
# class docx_to_text:
#     __name__ = "docx_to_text"
#     inputs = (
#         "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
#     )
#     output = "text/plain"

#     def __init__(self, name=None, **kwargs):
#         if name is not None:
#             self.__name__ = name

#     def name(self):
#         return self.__name__

#     def convert(self, orig, idata, **kwargs):
#         out = []
#         text = docx2txt.process(BytesIO(orig))
#         out.extend(self.clean_data(data=text))
#         idata.setData(" ".join(out))
#         return idata