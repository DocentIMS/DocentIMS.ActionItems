# -*- coding: utf-8 -*-


#from zope.publisher.browser import BrowserView
from plone.dexterity.browser.add import DefaultAddView
from plone.dexterity.browser.add import DefaultAddForm
from plone.dexterity.browser.edit import DefaultEditView
from plone.dexterity.browser.edit import DefaultEditForm

from zope.intid.interfaces import IIntIds
from z3c.relationfield import RelationValue
from plone import api
from zope.component import getUtility
from z3c.form import interfaces
from plone.app.versioningbehavior.behaviors import IVersionable
from zope.browserpage.viewpagetemplatefile import ViewPageTemplateFile as Z3ViewPageTemplateFile

from urllib.parse import unquote

from z3c.form import button


#from plone.app.textfield import RichText
#from zope.interface import Interface



class ActionItemsAddForm(DefaultAddForm):
    portal_type = "action_items"
    default_fieldset_label = 'Home'
    

    def __init__(self, context, request):
        super(ActionItemsAddForm, self).__init__(context, request)

    def updateWidgets(self):
        super(ActionItemsAddForm, self).updateWidgets()
        self.widgets['related_item'].mode = interfaces.HIDDEN_MODE
        self.widgets['IBasic.description'].mode = interfaces.HIDDEN_MODE
        self.widgets['IVersionable.changeNote'].mode = interfaces.HIDDEN_MODE       


    def updateFields(self):
        super(ActionItemsAddForm, self).updateFields()
        from_uid =  self.request.get('related_from')
        if not from_uid:
            from_url =  self.request.get('from_url')
            if from_url:
                portal_url= api.portal.get().absolute_url()
                from_path =    url = unquote(from_url).replace(portal_url, '')
                from_content = api.content.get(path=from_path)  
                from_uid = api.content.get_uuid(from_content)

        if from_uid:
            came_from  = api.content.get(UID=from_uid)
            initids = getUtility(IIntIds)
            came_from_i = initids.getId(came_from)
            self.fields['related_item'].field.default = RelationValue( came_from_i )

        to_uuid =  self.request.get('to_uuid')
        if to_uuid:
            self.fields['IBasic.description'].field.default = to_uuid
            

    def update(self):
        super(ActionItemsAddForm, self).update()
        

        for group in self.groups:
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
    ## Does not take portal type into action, so this is used FOR ALL
    portal_type = "action_items"
    default_fieldset_label = 'Home'
    
    
    def __init__(self, context, request):
        super(ActionItemsEditForm, self).__init__(context, request)

    def updateWidgets(self):
        super(ActionItemsEditForm, self).updateWidgets()
        
        #Hide input field 'change note'
        #if 'IVersionable.changeNote' in self.widgets
        if self.portal_type in  ['action_items', 'sow_analysis', 'project_companies', 'Document']:
            self.widgets['IVersionable.changeNote'].mode = interfaces.HIDDEN_MODE     
        
        if self.portal_type == 'action_items':
            self.widgets['IBasic.description'].mode = interfaces.HIDDEN_MODE
            
            
            # #import pdb; pdb.set_trace()
            # for group in self.groups:
            #     if group.__name__ == 'all_dates':
            #         self.groups['all_dates'].widgets['initial_due_date'].disabled='disabled'
            
        if self.portal_type == 'sow_analysis':
            #import pdb; pdb.set_trace()
            #self.widgets['bodytext'].template = Z3ViewPageTemplateFile("disabled_input.pt")
            #self.widgets['bodytext'].mode = interfaces.HIDDEN_MODE
            self.widgets['section_number'].readonly='readonly'
            self.widgets['IDublinCore.description'].mode = interfaces.HIDDEN_MODE
            
                    
        if self.portal_type == 'project_companies':
            self.widgets['IDublinCore.title'].label = 'Short Company Name'
            self.widgets['IDublinCore.description'].label = 'Full Company Name'
            self.widgets['IDublinCore.description'].template = Z3ViewPageTemplateFile("description_template.pt")

    
    def update(self):
        super(ActionItemsEditForm, self).update()
       
        if self.portal_type == 'action_items' or self.portal_type == 'sow_analysis':
            for group in self.groups:
                if group.__name__ == 'settings':
                    #group.mode = 'omitted'
                    group.label = None
                    group.widgets['IVersionable.versioning_enabled'].mode = interfaces.HIDDEN_MODE
                    group.widgets['IAllowDiscussion.allow_discussion'].mode = interfaces.HIDDEN_MODE

                if group.__name__ == 'all_dates':
                    #import pdb; pdb.set_trace()
                    #Not working
                    #group.widgets['initial_due_date'].disabled='disabled'
                    group.description = '{}<br/><p>Initial Due Date</p><input disabled class="form-control" value="{}"/>'.format(group.description , group.widgets['initial_due_date'].value)
                    group.widgets['initial_due_date'].mode = interfaces.HIDDEN_MODE

                if self.portal_type == 'sow_analysis':
                    if group.__name__ == 'settings' or group.__name__ == 'dates' or group.__name__ == 'categorization' or  group.__name__ == 'ownership':
                        #group.mode = 'omitted'
                        group.label = None
                    
                
                if group.__name__ == 'private_notes':
                        #if self.portal_type == 'action_items':
                        context = self.context
                        user =  api.user.get_current().getMemberId()
                        item = api.content.find(context=context, id=user, portal_type='personal_notes' )
                        
                        if item:
                            notes_item = item[0].getObject()
                            group.widgets['private_notes'].value = notes_item.bodytext 
                        else:
                            self.private_notes = None


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
        self.widgets['IDublinCore.description'].template = Z3ViewPageTemplateFile("description_template.pt")



    def updateFields(self):
        super(CompanyInformationAddForm, self).updateFields()

    def update(self):
        super(CompanyInformationAddForm, self).update()
        #self.fields['IDublinCore.title'].widgetFactory = TextWidget


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
        self.widgets['IDublinCore.title'].label = 'Short Company Name'
        self.widgets['IDublinCore.description'].label = 'Full Company Name'

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





class SowAnalysisAddForm(DefaultAddForm):
    portal_type = "sow_analysis"
    default_fieldset_label = 'Home'

    def __init__(self, context, request):
        super(SowAnalysisAddForm, self).__init__(context, request)

    def updateWidgets(self):
        super(SowAnalysisAddForm, self).updateWidgets()
        self.widgets['IDublinCore.description'].mode = interfaces.HIDDEN_MODE


    def updateFields(self):
        super(SowAnalysisAddForm, self).updateFields()
        
    def update(self):
        super(SowAnalysisAddForm, self).update()

        for group in self.groups:
            if group.__name__ == 'dates' or group.__name__ == 'categorization' or  group.__name__ == 'ownership':
                #group.mode = 'omitted'
                group.label = None
            if group.__name__ == 'settings':
                #group.mode = 'omitted'
                group.label = None
                group.widgets['IVersionable.versioning_enabled'].mode = interfaces.HIDDEN_MODE
                group.widgets['IAllowDiscussion.allow_discussion'].mode = interfaces.HIDDEN_MODE

class SowAnalysisAddFormView(DefaultAddView):
    form = SowAnalysisAddForm

# class SowAnalysisEditForm(DefaultEditForm):
#     portal_type = "sow_analysis"
#     default_fieldset_label = 'Home'

#     def __init__(self, context, request):
#         super(SowAnalysisEditForm, self).__init__(context, request)

#     def updateWidgets(self):
#         super(SowAnalysisEditForm, self).updateWidgets()
#         if self.portal_type == 'sow_analysis':
#             self.widgets['IBasic.description'].mode = interfaces.HIDDEN_MODE
            
#     def updateFields(self):
#         super(SowAnalysisEditForm, self).updateFields()

#     def update(self):
#         super(SowAnalysisEditForm, self).update()

#         if self.portal_type == 'sow_analysis':
#             for group in self.groups:
#                 if group.__name__ == 'settings' or group.__name__ == 'dates' or group.__name__ == 'categorization' or  group.__name__ == 'ownership':
#                     #group.mode = 'omitted'
#                     group.label = None
#                     group.widgets['IVersionable.versioning_enabled'].mode = interfaces.HIDDEN_MODE
#                     group.widgets['IAllowDiscussion.allow_discussion'].mode = interfaces.HIDDEN_MODE


# class SowAnalysisEditFormView(DefaultEditView):
#     portal_type = "sow_analysis"
#     default_fieldset_label = 'Home'
#     form = SowAnalysisEditForm
