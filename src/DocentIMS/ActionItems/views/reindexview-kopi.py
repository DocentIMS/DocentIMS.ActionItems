# -*- coding: utf-8 -*-

# from DocentIMS.ActionItems import _
from Products.Five.browser import BrowserView
from zope.interface import Interface
from plone import api



# from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile

#from plone.app.contentrules.api import get_rules
#from plone.contentrules.engine.assignments import RuleAssignmentManager 
#import getRules

from plone.contentrules.engine.interfaces import IRuleStorage
from zope.component import queryMultiAdapter
from plone.app.contentrules.handlers import execute




class IReindexView(Interface):
    """ Marker Interface for IProjectView"""


class ReindexView(BrowserView):
    # If you want to define a template here, please remove the template from
    # the configure.zcml registration of this view.
    # template = ViewPageTemplateFile('project_view.pt')

    def __call__(self):
        # Implement your own actions:
        return self.reindex()

    # def reindex(self):
    #     my_brains = self.context.portal_catalog(portal_type=['action_items', 'sow_analysis'])
    #     storage = queryUtility(IRuleStorage)
    #     storage.items()
    #     #getRules()
        
    #     for brain in my_brains:
            
 

    #         # Print the titles of the content rules
    #         # for rule in content_rules:
    #         #     print(rule['title'])
    #         old_urgency = brain.urgency
    #         brain.getObject().reindexObject(idxs=["daysleft", "urgency"])
    #        rules = get_rules(brain)
    #         for rule in rules:
    #                 if rule.enabled and rule.isAvailable(brain):
    #                     execute(rule, brain)
                
        
    #     return len(my_brains)

    def reindex(self):
        my_brains = self.context.portal_catalog(portal_type=['action_items', 'sow_analysis'])
        for brain in my_brains:
            old_urgency = brain.urgency
            brain.getObject().reindexObject(idxs=["daysleft", "urgency"])
            if brain.urgency != old_urgency:
                rules = get_rules(brain)
                for rule in rules:
                    if rule.enabled and rule.isAvailable(brain):
                        execute(rule, brain)
                
                #self.sendmailmessage(self, brain.urgency )
                
        
        return len(my_brains)
    
    #  def sendmailmessage(self, urgency):
    #     my_brains
