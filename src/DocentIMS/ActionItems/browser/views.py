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
#from plone.app.versioningbehavior.behaviors import IVersionable
from zope.browserpage.viewpagetemplatefile import ViewPageTemplateFile as Z3ViewPageTemplateFile

from urllib.parse import unquote

from z3c.form import button


	
from z3c.form.browser.textlines import TextLinesFieldWidget


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
        self.widgets['placeholder'].mode = interfaces.HIDDEN_MODE 
        self.widgets["placeholder"].disabled = "disabled"



    def updateFields(self):
        super(ActionItemsAddForm, self).updateFields()
        from_uid =  self.request.get('related_from')
        #self.from_uid =  self.request.get('related_from')
        to_uuid =  self.request.get('to_uuid')
        exp_text =  self.request.get('exp_text')
        if not from_uid:
            from_url =  self.request.get('from_url')
            if from_url and from_url != '':
                portal_url= api.portal.get().absolute_url()
                from_path =  from_url.replace(portal_url, '')
                from_content = api.content.get(path=from_path)  
                from_uid = api.content.get_uuid(from_content)

        if from_uid:
            came_from  = api.content.get(UID=from_uid)
            initids = getUtility(IIntIds)
            came_from_i = initids.getId(came_from)
            self.fields['related_item'].field.default = RelationValue( came_from_i )

        
        if to_uuid:
            self.fields['placeholder'].field.default = to_uuid
            #import pdb; pdb.set_trace()
            # self.fields['IBasic.description'].field.default = to_uuid

        if exp_text:
            #self.fields['full_explanation'].field.default = exp_text
            # title is only 40 characters
            #self.fields['IBasic.title'].field.default = exp_text[:39]
            self.fields['full_explanation'].field.default = exp_text
            
        for group in self.groups:
            if group.__name__ == 'connections':
                if from_uid:
                    camefrom = api.content.get(UID=from_uid)
                    if camefrom.Type() == 'Scope Breakdown':
                        group.fields['related_sow_section'].field.default = from_uid

            
            

    def update(self): 
        super(ActionItemsAddForm, self).update()
        

        for group in self.groups:
            if group.__name__ == 'close_out' or group.__name__ == 'intermediate_actioins':
                #group.mode = 'omitted'
                group.label = None
                
                
            # if group.__name__ == 'connections':
            #     from_uid =  self.request.get('related_from')
            #     if not from_uid:
            #         from_url =  self.request.get('from_url')
            #         if from_url and from_url != '':
            #             portal_url= api.portal.get().absolute_url()
            #             from_path =  from_url.replace(portal_url, '')
            #             from_content = api.content.get(path=from_path)  
            #             from_uid = api.content.get_uuid(from_content)
                        
            #     group.fields['related_sow_section'].field.default = from_uid
            
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
            self.widgets['placeholder'].mode = interfaces.HIDDEN_MODE 
            self.widgets["placeholder"].disabled = "disabled"
            
            # #import pdb; pdb.set_trace()
            # for group in self.groups:
            #     if group.__name__ == 'all_dates':
            #         self.groups['all_dates'].widgets['initial_due_date'].disabled='disabled'
            
        if self.portal_type == 'sow_analysis':
            # add confition to only show edit field for admins etc.
            user = api.user.get_current()
            #groups = api.group.get_groups(user=user) 
            #group = api.group.get('PrjMgr')
            roles = api.user.get_roles()
            #member_ids = [member.getId() for member in group.getGroupMembers()]
            #Just checking for user in usergroup strangly does not work              
            #if not user.id in member_ids:
            if not 'Project Manager' in roles:
                self.widgets['bodytext'].mode = interfaces.DISPLAY_MODE
            self.widgets['section_number'].readonly='readonly'
            self.widgets['IDublinCore.description'].mode = interfaces.HIDDEN_MODE
            
                    
        if self.portal_type == 'project_companies':
            self.widgets['IDublinCore.title'].label = 'Short Company Name'
            self.widgets['IDublinCore.description'].label = 'Full Company Name'
            self.widgets['IDublinCore.description'].template = Z3ViewPageTemplateFile("description_template.pt")

        if self.portal_type == 'Meeting' or self.portal_type == 'meeting':
            self.widgets['IEventBasic.whole_day'].mode = interfaces.HIDDEN_MODE
            self.widgets['IEventBasic.open_end'].mode = interfaces.HIDDEN_MODE
    
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






class MeetingEditForm(DefaultEditForm):
    ## Does not take portal type into action, so this is used FOR ALL content items that are defined as 'Item'
    portal_type = "Meeting"
     
     
    def __init__(self, context, request):
        super(MeetingEditForm, self).__init__(context, request)

    def updateWidgets(self):
        super(MeetingEditForm, self).updateWidgets()
         
        if self.portal_type == "Meeting" or self.portal_type == 'meeting':
            self.widgets['IEventBasic.whole_day'].mode = interfaces.HIDDEN_MODE
            self.widgets['IEventBasic.open_end'].mode = interfaces.HIDDEN_MODE
            self.widgets['IBasic.description'].mode = interfaces.HIDDEN_MODE
            #self.widgets['IVersionable.changeNote'].mode = interfaces.HIDDEN_MODE  
     
    def update(self):
        super(MeetingEditForm, self).update()
        
        if self.portal_type in  ["Meeting", "meeting", "Notes", "notes", "Feedback", "feedback"]:
        
            for group in self.groups:
                if group.__name__ == 'settings':
                    group.label = None
                    #group.widgets['IVersionable.versioning_enabled'].mode = interfaces.HIDDEN_MODE
                    group.widgets['IAllowDiscussion.allow_discussion'].mode = interfaces.HIDDEN_MODE
                    
                    
                if group.__name__ == 'settings' or group.__name__ == 'dates' or group.__name__ == 'categorization' or  group.__name__ == 'ownership':
                    #group.mode = 'omitted'
                    group.label = None
            
        
        
         

class MeetingEditFormView(DefaultEditView):
    portal_type = "Meeting"
    form = MeetingEditForm

 




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




class MeetingAddForm(DefaultAddForm):

    #portal_type = "Meeting"
    
    def __init__(self, context, request):
        super(MeetingAddForm, self).__init__(context, request)

    def updateWidgets(self):
        super(MeetingAddForm, self).updateWidgets()
        if self.portal_type == 'Meeting' or self.portal_type == 'meeting':
            self.widgets['IEventBasic.whole_day'].mode = interfaces.HIDDEN_MODE
            self.widgets['IEventBasic.open_end'].mode = interfaces.HIDDEN_MODE
            
        if self.portal_type in  ["Meeting", "meeting", "Notes", "Feedback"]:
            self.widgets['IBasic.description'].mode = interfaces.HIDDEN_MODE
            #self.widgets['IVersionable.changeNote'].mode = interfaces.HIDDEN_MODE  


    def updateFields(self):
        super(MeetingAddForm, self).updateFields()
        
    def update(self):
        super(MeetingAddForm, self).update()
        
        if self.portal_type in  ["Meeting", "meeting", "Notes", "Feedback"]:
            for group in self.groups:
                if group.__name__ == 'settings':
                    group.label = None
                    #group.widgets['IVersionable.versioning_enabled'].mode = interfaces.HIDDEN_MODE
                    group.widgets['IAllowDiscussion.allow_discussion'].mode = interfaces.HIDDEN_MODE
            
                if group.__name__ == 'settings' or group.__name__ == 'dates' or group.__name__ == 'categorization' or  group.__name__ == 'ownership':
                    #group.mode = 'omitted'
                    group.label = None
        


class MeetingAddFormView(DefaultAddView):
    form = MeetingAddForm


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
