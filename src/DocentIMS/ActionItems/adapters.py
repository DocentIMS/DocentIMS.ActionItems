# -*- coding: utf-8 -*-

from zope.interface import Interface
from zope.component import adapter
from plone.stringinterp.adapters import BaseSubstitution

@adapter(Interface)
class AssignedTo(BaseSubstitution):
    category = "All Content"
    description = "Assigned To"

    def safe_call(self):
      if hasattr(self.context, 'assigned_to'):
        return self.context.assigned_to
      return ''

        
# @adapter(Interface)
# class DueDate(BaseSubstitution):
#     category = "All Content"
#     description = "Due Date"

#     def safe_call(self):
#       #import pdb; pdb.set_trace()
#       if hasattr(self.context, 'initial_due_date'):
#         return self.context.revised_due_date or self.context.initial_due_date
#       return ''       
        

