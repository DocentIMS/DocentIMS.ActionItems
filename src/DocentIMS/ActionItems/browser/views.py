from zope.publisher.browser import BrowserView
from plone.dexterity.browser.add import DefaultAddView
from plone.dexterity.browser.add import DefaultAddForm
from plone.dexterity.browser.edit import DefaultEditView
from plone.dexterity.browser.edit import DefaultEditForm
from plone.uuid.interfaces import IUUID
from zope.intid.interfaces import IIntIds
from Products.CMFCore.utils import getToolByName
from z3c.relationfield import RelationValue
from plone import api

from zope.component import getUtility

#from zope.lifecycleevent import modified
import transaction
from bs4 import BeautifulSoup



class ActionItemsAddForm(DefaultAddForm):
    portal_type = "action_items"
    default_fieldset_label = 'Home'

    def __init__(self, context, request):
        super(ActionItemsAddForm, self).__init__(context, request)

    def updateFields(self):
        super(ActionItemsAddForm, self).updateFields()
        from_uid =  self.request.get('related_from')

        if from_uid:
            came_from  = api.content.get(UID=from_uid)
            initids = getUtility(IIntIds)
            came_from_i = initids.getId(came_from)

            #import pdb; pdb.set_trace()
            self.fields['related_item'].field.default = RelationValue( came_from_i )
            #self.fields['related_item'].field.default_value = RelationValue( came_from_i )

    def update(self):
        super(ActionItemsAddForm, self).update()

class ActionItemsEditForm(DefaultEditForm):
    default_fieldset_label = 'Home'

class ActionItemsAddFormView(DefaultAddView):
    form = ActionItemsAddForm

class ActionItemsEditFormView(DefaultEditView):
    form = ActionItemsEditForm
