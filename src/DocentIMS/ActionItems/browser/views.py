

from zope.publisher.browser import BrowserView
from plone.dexterity.browser.add import DefaultAddView
from plone.dexterity.browser.add import DefaultAddForm
from plone.dexterity.browser.edit import DefaultEditView
from plone.dexterity.browser.edit import DefaultEditForm
from plone.dexterity.browser import edit
from plone.uuid.interfaces import IUUID
from zope.intid.interfaces import IIntIds
from Products.CMFCore.utils import getToolByName
from z3c.relationfield import RelationValue
from plone import api
from zope.component import getUtility
from z3c.form import interfaces
from plone.app.versioningbehavior.behaviors import IVersionable

class ActionItemsAddForm(DefaultAddForm):
    portal_type = "action_items"
    default_fieldset_label = 'Home'

    def __init__(self, context, request):
        super(ActionItemsAddForm, self).__init__(context, request)

    def updateWidgets(self):
        super(ActionItemsAddForm, self).updateWidgets()
        self.widgets['related_item'].mode = interfaces.HIDDEN_MODE
        self.widgets['IBasic.description'].mode = interfaces.HIDDEN_MODE


    def updateFields(self):
        super(ActionItemsAddForm, self).updateFields()
        from_uid =  self.request.get('related_from')

        if from_uid:
            came_from  = api.content.get(UID=from_uid)
            initids = getUtility(IIntIds)
            came_from_i = initids.getId(came_from)
            self.fields['related_item'].field.default = RelationValue( came_from_i )

    def update(self):
        super(ActionItemsAddForm, self).update()

        for group in self.groups:
            #import pdb; pdb.set_trace()
            if group.__name__ == 'settings':
                #group.mode = 'omitted'
                group.label = None
                group.widgets['IVersionable.versioning_enabled'].mode = interfaces.HIDDEN_MODE
                group.widgets['IAllowDiscussion.allow_discussion'].mode = interfaces.HIDDEN_MODE

class ActionItemsAddFormView(DefaultAddView):
    form = ActionItemsAddForm

class ActionItemsEditForm(DefaultEditForm):
    portal_type = "action_items"
    default_fieldset_label = 'Home'

    def __init__(self, context, request):
        super(ActionItemsEditForm, self).__init__(context, request)

    def updateWidgets(self):
        super(ActionItemsEditForm, self).updateWidgets()
        if self.portal_type == 'action_items':
            self.widgets['IBasic.description'].mode = interfaces.HIDDEN_MODE
            #self.widgets['related_item'].mode = interfaces.HIDDEN_MODE

    def updateFields(self):
        super(ActionItemsEditForm, self).updateFields()

    def update(self):
        super(ActionItemsEditForm, self).update()

        if self.portal_type == 'action_items':
            for group in self.groups:
                #import pdb; pdb.set_trace()
                if group.__name__ == 'settings':
                    #group.mode = 'omitted'
                    group.label = None
                    group.widgets['IVersionable.versioning_enabled'].mode = interfaces.HIDDEN_MODE
                    group.widgets['IAllowDiscussion.allow_discussion'].mode = interfaces.HIDDEN_MODE


class ActionItemsEditFormView(DefaultEditView):
    portal_type = "action_items"
    default_fieldset_label = 'Home'
    form = ActionItemsEditForm
