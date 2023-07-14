

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
from z3c.form.browser.text import TextWidget

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
            if group.__name__ == 'close_out' or group.__name__ == 'intermediate_actioins':
                #group.mode = 'omitted'
                group.label = None
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





class CompanyInformationAddForm(DefaultAddForm):
    portal_type = "project_companies"
    default_fieldset_label = 'Company'

    def __init__(self, context, request):
        super(CompanyInformationAddForm, self).__init__(context, request)

    def updateWidgets(self):
        super(CompanyInformationAddForm, self).updateWidgets()
        self.widgets['IDublinCore.title'].label = 'Short Company Name'
        self.widgets['IDublinCore.description'].label = 'Full Company Name'
        #self.fields['IDublinCore.description'].widgetFactory = TextWidget
        #self.fields['IDublinCore.title'].widgetFactory = TextWidget

        #self.fields['IDublinCore.description'].widgetFactory = TextWidget
        #self.fields['IDublinCore.description'].widget = TextWidget


    def updateFields(self):
        super(CompanyInformationAddForm, self).updateFields()
        #self.widgets['IDublinCore.description'].rows = 1
        #self.fields['IDublinCore.description'].widgetFactory = TextWidget


        #import pdb; pdb.set_trace()
        #self.fields['IDublinCore.description'].widgetFactory = TextWidget

    def update(self):
        super(CompanyInformationAddForm, self).update()
        #self.fields['IDublinCore.description'].widgetFactory = TextWidget
        self.fields['IDublinCore.title'].widgetFactory = TextWidget

        for group in self.groups:
            if group.__name__ == 'settings':
                #group.mode = 'omitted'
                group.label = None
                group.widgets['IVersionable.versioning_enabled'].mode = interfaces.HIDDEN_MODE
                group.widgets['IAllowDiscussion.allow_discussion'].mode = interfaces.HIDDEN_MODE

class CompanyInformationAddFormView(DefaultAddView):
    form = CompanyInformationAddForm

class CompanyInformationEditForm(DefaultEditForm):
    portal_type = "project_companies"
    default_fieldset_label = 'Company'

    def __init__(self, context, request):
        super(CompanyInformationEditForm, self).__init__(context, request)

    def updateWidgets(self):
        super(CompanyInformationEditForm, self).updateWidgets()
        if self.portal_type == 'company_information':
            self.widgets['IBasic.description'].label = 'Short Company Name'

    def updateFields(self):
        super(CompanyInformationEditForm, self).updateFields()

    def update(self):
        super(CompanyInformationEditForm, self).update()

        if self.portal_type == 'project_companies':
            for group in self.groups:
                if group.__name__ == 'settings':
                    #group.mode = 'omitted'
                    group.label = None
                    group.widgets['IVersionable.versioning_enabled'].mode = interfaces.HIDDEN_MODE
                    group.widgets['IAllowDiscussion.allow_discussion'].mode = interfaces.HIDDEN_MODE


class CompanyInformationEditFormView(DefaultEditView):
    portal_type = "project_companies"
    default_fieldset_label = 'Company'
    form = CompanyInformationEditForm
