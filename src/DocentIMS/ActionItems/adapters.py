# -*- coding: utf-8 -*-

from zope.interface import Interface
from zope.component import adapter
from plone.stringinterp.adapters import BaseSubstitution
from plone import api

from DocentIMS.ActionItems.interfaces import IDocentimsSettings


@adapter(Interface)
class AssignedTo(BaseSubstitution):
    category = "All Content"
    description = "Assigned To"

    def safe_call(self):
      if hasattr(self.context, 'assigned_to'):
        return self.context.assigned_to
      return ''

class DaysLeft(BaseSubstitution):
    category = "All Content"
    description = "Assigned To"

    def safe_call(self):
      if hasattr(self.context, 'daysleft'):
        return self.context.daysleft
      return ''

@adapter(Interface)
class AssignedMail(BaseSubstitution):
    category = "All Content"
    description = "Assigned To Email"

    def safe_call(self):
      if hasattr(self.context, 'assigned_to'):
        #return assigned users email
        return api.user.get(userid=self.context.assigned_to).getProperty('email')
      
      return ''


@adapter(Interface)
class AssignedFullName(BaseSubstitution):
    category = "All Content"
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
#       #import pdb; pdb.set_trace()
#       if hasattr(self.context, 'initial_due_date'):
#         return self.context.revised_due_date or self.context.initial_due_date
#       return ''       
        

