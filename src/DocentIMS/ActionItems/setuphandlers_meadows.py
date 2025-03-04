# -*- coding: utf-8 -*-
from Products.CMFPlone.interfaces import INonInstallable
from Products.CMFCore.utils import getToolByName
from zope.interface import implementer
#from plone import api
import os
from plone.namedfile.file import NamedBlobImage
from plone.namedfile.file import NamedBlobFile

from plone.base.interfaces import constrains
from plone.base.interfaces.constrains import IConstrainTypes
from plone.base.interfaces.constrains import ISelectableConstrainTypes

import pandas as pd
import openpyxl
from zope.lifecycleevent import modified
import plone.api
from zope.component.hooks import setSite
import transaction


from pandas import *

import datetime

import os



#from plone.base.interfaces.constrains import ISelectableConstrainTypes
#from plone.base.interfaces.constrains import ISelectableConstrainTypes as IESelectableConstrainTypes
#from plone.app.dexterity.behaviors.constrains import ConstrainTypesBehavior

#from plone.app.dexterity.behaviors import constrains
#from plone.app.dexterity.behaviors.constrains.ConstrainTypesBehavior import getDefaultAddableTypes

#from plone.app.dexterity.behaviors.constrains.ConstrainTypesBehavior  import
#getConstrainTypesMode, getDefaultAddableTypes, getLocallyAllowedTypes, setLocallyAllowedTypes


@implementer(INonInstallable)
class HiddenProfiles(object):

    def getNonInstallableProfiles(self):
        """Hide uninstall profile from site-creation and quickinstaller."""
        return [
            "DocentIMS.ActionItems:uninstall",
        ]

    def getNonInstallableProducts(self):
        """Hide the upgrades package from site-creation and quickinstaller."""
        return ["DocentIMS.ActionItems.upgrades"]


def post_install(context):
    """Post install script"""
    # Do something at the end of the installation of this package.

    
    portal = plone.api.portal.get()
    
    plone.api.user.create(email='wglover@docentims.com', username='wglover@docentims.com', password=None, roles=('Member', 'Manager',), properties={'fullname': "Wayne Glover", 'first_name': 'Wayne', 'last_name': 'Glover'})
    plone.api.user.create(email='espen@medialog.no', username='espen@medialog.no', password=None, roles=('Member', 'Manager',), properties={'fullname': "Espen Moe-Nilssen", 'first_name': 'Espen', 'last_name': 'MN'})
    plone.api.group.add_user(groupname='PrjTeam', username='wglover@docentims.com')
    
    #Assign roles
    plone.api.group.grant_roles(groupname='PrjMgr', roles=['Board President', 'Edit Controlpanel'])
    plone.api.group.grant_roles(groupname='PrjTeam', roles=['Member', 'Reader'])
    
    #plone.api.group.grant_roles(groupname='can_parse', roles=['Project Manager'])
    #plone.api.group.grant_roles(groupname='can_command_statements', roles=['Project Manager'])
    #plone.api.group.grant_roles(groupname='can_document_manager', roles=['Project Manager'])
    
    # permission = 'plone.app.controlpanel.UsersAndGroups'
    # roles_to_grant = ['Manager']  # or whatever role you want to grant
    # portal.rolesOfPermission(permission).addRole('Manager', 'PrjMgr')
    # plone.app.controlpanel.UsersAndGroups
    # plone.api.group.grant_roles(groupname='PrjMgr', roles=['Edit Controlpanel'])
  
    
    
    #Set control panel properties, since we can not set them TTW
    #TODO: Maybe make a check 
    
    plone.api.portal.set_registry_record('DocentIMS.ActionItems.interfaces.IDocentimsSettings.location_names', 
                                         [{'location_name': 'Zoom'}, 
                                          {'location_name': 'Clubhouse'},
                                          {'location_name': 'Clubhouse and Zoom'}
                                         ])
    
    
    plone.api.portal.set_registry_record('DocentIMS.ActionItems.interfaces.IDocentimsSettings.table_columns', 
                                         [{'row_field': 'actionno', 'row_title': 'ID'}, 
                                          {'row_field': 'title', 'row_title': 'Title'},
                                          {'row_field': 'assigned_to', 'row_title': 'Responsible person'},
                                          {'row_field': 'duedate', 'row_title': 'Due date'}
                                         ])
    
    plone.api.portal.set_registry_record('DocentIMS.ActionItems.interfaces.IDocentimsSettings.scope_table_columns',
                                        [  {'row_field': 'section_number', 'row_title': 'ID'}, 
                                           {'row_field': 'title', 'row_title': 'Title'}, 
                                           {'row_field': 'duedate', 'row_title': 'Due date'}, 
                                           {'row_field': 'estimated_qc_time', 'row_title': 'Estimated QC'} 
                                            ]
                                       )
    
    
    plone.api.portal.set_registry_record('DocentIMS.ActionItems.interfaces.IDocentimsSettings.vokabularies',
                                        [{'vocabulary_entry': 'President'},
                                         {'vocabulary_entry': 'Secretary'},
                                         {'vocabulary_entry': 'Treasurer'}, 
                                         {'vocabulary_entry': 'At Large'}, 
                                        ])
    

    plone.api.portal.set_registry_record('DocentIMS.ActionItems.interfaces.IDocentimsSettings.vokabularies3',
                                        [   {'vocabulary_entry': 'Prime'},
                                            {'vocabulary_entry': 'Architect'},
                                            {'vocabulary_entry': 'Geotechnical'},
                                            {'vocabulary_entry': 'Outreach'},
                                            {'vocabulary_entry': 'Property Manager'},                                            
                                        ])  
    
    plone.api.portal.set_registry_record('DocentIMS.ActionItems.interfaces.IDocentimsSettings.meeting_types',
      [ {'meeting_type': 'Board-Only Meeting', 
         'meeting_title': 'Board Members Only Meeting', 
         'meeting_summary': 'This meeting is only for board members and is used to work on specific work.', 
         'meeting_attendees': {'PrjTeam'}, 
         'meeting_contact': 'wglover@docentims.com'},
        {'meeting_type': 'Community Meeting', 
         'meeting_title': 'Meadows Community Meeting', 
         'meeting_summary': 'Monthly board meeting with all residents invited.', 
         'meeting_attendees': {'PrjTeam'}, 
         'meeting_contact': 'wglover@docentims.com'},
        {'meeting_type': 'Executive Session', 
         'meeting_title': 'Board Executive Session', 
         'meeting_summary': 'Board-only discussions', 
         'meeting_attendees': {'PrjTeam'}, 
         'meeting_contact': 'wglover@docentims.com'},
      ])
    
 

    # plone.api.portal.set_registry_record('DocentIMS.ActionItems.interfaces.IDocentimsSettings.companies',
    #                                     [{'full_company_name': 'Parametrix, Inc.',
    #                                       'short_company_name': 'Parametrix' ,
    #                                       'company_letter_kode': 'PMX',
    #                                       'company_role': None,
    #                                       'company_full_street_address': '719 2nd Avenue',
    #                                       'company_other_address': 'Suite 200',
    #                                       'company_city': 'Seattl',
    #                                       'company_state': 'WA',
    #                                       'company_zip': '98104'}, 
    #                                      {'full_company_name': 'Docent IMS LLC',
    #                                       'short_company_name': 'Docent' ,
    #                                       'company_letter_kode': 'DOC',
    #                                       'company_role': None,
    #                                       'company_full_street_address': '141 Reservoir Ave',
    #                                       'company_other_address': '',
    #                                       'company_city': 'Revere',
    #                                       'company_state': 'MA',
    #                                       'company_zip': '02151'},
    #                                     ])
    
    
    
                                          
                                          
    # Create Folder to put everything in
    _create_content(portal)
    if not portal.get('frontpage', False):
        fpage = plone.api.content.create(
            type='FrontPage',
            container=portal,
            id='frontpage',
            title='Front page' 
        )
        plone.api.content.transition(obj=portal['frontpage'], transition='publish')
        
    portal.default_page='frontpage'
    
    #Restrict content types that can be added to folders
    action_folder = portal.get('action-items', False)
    behaviour = constrains.ISelectableConstrainTypes(action_folder)
    behaviour.setConstrainTypesMode(constrains.ENABLED)
    behaviour.setImmediatelyAddableTypes(['action_items', 'Collection'])
    behaviour.setLocallyAllowedTypes(['action_items', 'Collection'])

    # scope_analysis = portal.get('scope-analysis', False)
    # behaviour = constrains.ISelectableConstrainTypes(scope_analysis)
    # behaviour.setConstrainTypesMode(constrains.ENABLED)
    # behaviour.setImmediatelyAddableTypes(['sow_analysis'])
    # behaviour.setLocallyAllowedTypes(['sow_analysis'])
    
    # notes = portal.get('notes', False)
    # behaviour = constrains.ISelectableConstrainTypes(notes)
    # behaviour.setConstrainTypesMode(constrains.ENABLED)
    # behaviour.setImmediatelyAddableTypes(['otes',])
    # behaviour.setLocallyAllowedTypes(['Notes'])
    
    feedback = portal.get('feedback', False)
    behaviour = constrains.ISelectableConstrainTypes(feedback)
    behaviour.setConstrainTypesMode(constrains.ENABLED)
    behaviour.setImmediatelyAddableTypes(['feedback'])
    behaviour.setLocallyAllowedTypes(['feedback'])

    meeting = portal.get('meeting', False)
    behaviour = constrains.ISelectableConstrainTypes(meeting)
    behaviour.setConstrainTypesMode(constrains.ENABLED)
    behaviour.setImmediatelyAddableTypes(['meeting'])
    behaviour.setLocallyAllowedTypes(['meeting'])

def pre_install(context):
    """Pre install script"""
    # Do something before the installation of this package.
    portal = plone.api.portal.get()
    
    #create groups, wayne might need these for workflow
    #plone.api.group.create(groupname="PrjCust", title="Project Customer", description="The customer for the project")
    plone.api.group.create(groupname="PrjMgr", title="Board President", description="Board President")
    plone.api.group.create(groupname="PrjTeam", title="Meadows Board", description="All Members of the Meadows Board")
    #plone.api.group.create(groupname="PrjQcMgr", title="Project QC Manager", description="Person in charge of manage QC for the project")
    
    #plone.api.group.create(groupname="can_parse", title="Can parse in Word", description="Can parse in Word")
    #plone.api.group.create(groupname="can_command_statements", title="Can Command Statements in Word")
    #plone.api.group.create(groupname="can_document_manager", title="Can Document Manager in Word")
    
    #plone.api.group.create(groupname="docentMtgAgenda", title="Can Add Meeting Agenda")
    #plone.api.group.create(groupname="docentLetter", title="Can Add Letter")
    
    # plone.api.group.create(groupname="docentMtgMin", title="Can Add Meeting Minutes")
    # plone.api.group.create(groupname="docentMemo", title="Can Add Memo")
    # plone.api.group.create(groupname="can_parse", title="Can Parse in Word")
    #plone.api.group.create(groupname="can_add_project_scope", title="Can Add Scope")
    #plone.api.group.create(groupname="can_command_statements", title="Can Command Statements")
     
    plone.api.group.create(groupname="can_modify_templates", title="Can Modify Templates", description="Controls who can modify the templates used in Word to create Docent documents.")
    plone.api.group.create(groupname="can_add_planning_document", title="Can Add Planning Document", description="Planning documents are those reviewed when the Project is still in Planning phase.  These documents are to help prepare to study the project.")
    plone.api.group.create(groupname="can_add_meeting_agenda", title="Can Add Meeting Agenda", description="People allowed to add agenda.  This is separate from users who can add meetings.  I expect the board to be able to add minutes, but only President allowed to add meeting.")
    plone.api.group.create(groupname="can_add_meeting_minutes", title="Can Add Meeting Minutes", description="People allowed to add Minutes.  This is separate from users who can add meetings.  I expect the board to be able to add minutes, but only President allowed to add meeting.")
    plone.api.group.create(groupname="can_add_documents", title="Can Add Documents", description="Top level control over who can add any document.")
    plone.api.group.create(groupname="can_add_meeting", title="Can Add Meetings", description="People allowed to add Meeting.  This is separate from users who can add agenda, minutes, etc.  I expect the board to be able to add minutes, but only President allowed to add meeting.")
    
    
    
    
   
 
    #create content 
    
    _create_content(portal)
    _create_more_content(portal)



def post_import(context):
    """Post install script"""
    # Do something at the end of the installation of this package.
    
    portal = plone.api.portal.get()
    
    #Set control panel properties, since we can not set them TTW
    #TODO: Maybe make a check 
    #plone.api.portal.set_registry_record('DocentIMS.ActionItems.interfaces.IDocentimsSettings.table_columns', [{'row_field': 'actionno', 'row_title': 'ID'}, {'row_field': 'title', 'row_title': 'Title'}])
    #plone.api.portal.set_registry_record('DocentIMS.ActionItems.interfaces.IDocentimsSettings.scope_table_columns',  [{'row_field': 'id', 'row_title': 'ID'}, {'row_field': 'title', 'row_title': 'Title'}])
    

    #Import excel content    
    # _import_content(portal)
    

def _create_content(portal):
        
        #folderpath = os.path.dirname(__file__)
        #fullpath = "{folderpath}/ai_import.xlsx".format(folderpath=folderpath)
        
        #delete news folder
        if portal.get('news', False):
            folder = portal.get('news', False)
            plone.api.content.delete(obj=folder)

        if portal.get('events', False):
            folder = portal.get('events', False)
            plone.api.content.delete(obj=folder)
            
            

        folder = portal.get('Members', False)
        folder.title= 'Team'
        folder.reindexObject(idxs=['Title'])
            
            
            

        if not portal.get('action-items', False):
            action_items = plone.api.content.create(
                type='Folder',
                container=portal,
                id='action-items',
                title='Tasks',
                layout='action-overview',
                default_page='action-items-collection',
                nextPreviousEnabled=1 
            )
            
            ## add collection inside here
            

            if not action_items.get('action-items-collection', False):
                action_items_collection = plone.api.content.create(
                    type='Collection',
                    container=action_items,
                    id='action-items-collection',
                    title='Tasks',
                    layout='action-overview',
                    query = [{'i': 'portal_type', 'o': 'plone.app.querystring.operation.selection.any', 'v': ['action_items']}],
                    limit=2000,
                    item_count=500,
                )
                
                
                
        
                
        if not portal.get('meeting', False):
            meeting = plone.api.content.create(
                type='Folder',
                container=portal,
                id='meeting',
                title='Meetings',
                default_page='meeting-collection',
                nextPreviousEnabled=0
            )
            
            ## add collection inside
            
            if not meeting.get('meeting-collection', False):
                meeting_collection = plone.api.content.create(
                    type='Collection',
                    container=meeting,
                    id='meeting-collection',
                    title='Meetings',
                    layout="card_view",
                    query = [{'i': 'portal_type', 'o': 'plone.app.querystring.operation.selection.any', 'v': ['meeting', 'Meeting']}]
                )
                                
                
        if not portal.get('documents', False):
            images_folder = plone.api.content.create(
                type='Folder',
                container=portal,
                id='documents',
                title='Documents',
            )  
            
        # if not portal.get('documents', False):
        #     images_folder = plone.api.content.create(
        #         type='Folder',
        #         container=portal,
        #         id='documents',
        #         title='Documents',
        #     )
            
        if not portal.get('postit_notes', False):
            postit_notes = plone.api.content.create(
                type='Folder',
                container=portal,
                id='postit_notes',
                title='PostIt Notes',
                default_page='postit-collection',
                exclude_from_nav=True,
            )  
            
            if not postit_notes.get('postit-collection', False):
                postit_collection = plone.api.content.create(
                    type='Collection',
                    container=postit_notes,
                    id='postit-collection',
                    title='Post It Notes',
                    query = [
                        {'i': 'portal_type', 'o': 'plone.app.querystring.operation.selection.any', 'v': ['postit_notes', 'postit_note', 'PostIt Notes']},
                        { "i":"Creator",  "o":"plone.app.querystring.operation.string.currentUser", "v":""  }
                        ]
                )
                         
                
        # if not portal.get('notes', False):
        #     notes = plone.api.content.create(
        #         type='Folder',
        #         container=portal,
        #         id='notes',
        #         title='Notes',
        #         default_page='notes-collection',
        #         nextPreviousEnabled=1
        #     )
            
            ## add collection inside
            
            

            # if not notes.get('notes-collection', False):
            #     notes_collection = plone.api.content.create(
            #         type='Collection',
            #         container=notes,
            #         id='notes-collection',
            #         title='Notes',
            #         layout='tabular_view',
            #         limit=2000,
            #         item_count=500,
            #         customViewFields = ['Title', 'CreationDate'],
            #         query = [{'i': 'portal_type', 'o': 'plone.app.querystring.operation.selection.any', 'v': ['Notes']}]
            #     )
                            
                
        if not portal.get('feedback', False):
            feedback = plone.api.content.create(
                type='Folder',
                container=portal,
                id='feedback',
                title='Feedback',
                default_page='feedback-collection',
                nextPreviousEnabled=1
            )
            
            ## add collection inside
            
            

            if not feedback.get('feedback-collection', False):
                feedback_collection = plone.api.content.create(
                    type='Collection',
                    container=feedback,
                    id='feedback-collection',
                    title='Feedback',
                    description=u"""These are comments submitted by users of this website and Word Docent toolbar. The project manager should review all feedback items and respond if requested by the person submitting the Feedback""",
                    layout='tabular_view',
                    limit=2000,
                    item_count=500,
                    customViewFields = ['Title', 'Creator', 'CreationDate', 'review_state'],
                    query = [{'i': 'portal_type', 'o': 'plone.app.querystring.operation.selection.any', 'v': ['feedback']}]
                )
                
        if not portal.get('planning-documents', False):
            planning_documents = plone.api.content.create(
                type='Folder',
                container=portal,
                id='planning-documents',
                title='Planning Documents',
                description="This folder holds all the documents and parsed sections of all planning documents.",
                default_page='planning-collection',
                nextPreviousEnabled=1
            )
            
            ## add collection inside

            if not planning_documents.get('planning-collection', False):
                planning_collection = plone.api.content.create(
                    type='Collection',
                    container=planning_documents,
                    id='planning-collection',
                    title='Planning Documents',
                    description="This folder holds all the documents and parsed sections of all planning documents.",
                    layout='tabular_view',
                    limit=2000,
                    item_count=500,
                    customViewFields = ['Title', 'Creator', 'CreationDate', 'review_state'],
                    query = [{'i': 'portal_type', 'o': 'plone.app.querystring.operation.selection.any', 'v': ['Planning Document']}]
                )      
        
                
        if not portal.get('site-collections', False):
            items = plone.api.content.create(
                type='Folder',
                container=portal,
                id='site-collections',
                title='Site Collections',
                exclude_from_nav=False,
        )
            
        if not portal.get('calendar', False):
            items = plone.api.content.create(
                type='Folder',
                container=portal,
                description="To get this calendar:  add a collection with Meetings.  When viewing the collection,  click on : Actions-> Enable fullcalender and choose Fullcalender as the view",
                id='calendar',
                title='Calendar',
                exclude_from_nav=False,
        )
            
        if not portal.get('word-makro', False):
            items = plone.api.content.create(
                type='Folder',
                container=portal,
                description="This has the macros from Abdallah",
                id='word-makro',
                title='Word Macro',
                exclude_from_nav=True,
        )
            
            
            
            

            
        #     collection-of-collections = plone.api.content.create(
        #             type='Collection',
        #             container=feedback,
        #             id='feedback-collection',
        #             title='Feedback',
        #             description=u"""  This collects all the collections on the site.   This helps me keep track of the collections i have and where they are.  helps avoid duplication.""",
        #             layout='tabular_view',
        #             limit=2000,
        #             item_count=500,
        #             customViewFields = ['Title', 'Creator', 'CreationDate', 'review_state'],
        #             query = [{'i': 'portal_type', 'o': 'plone.app.querystring.operation.selection.any', 'v': ['feedback']}]
        #         )
                
       
            
            
            
                

        
        if not portal.get('help-files', False):
            items = plone.api.content.create(
                type='Folder',
                container=portal,
                id='help-files',
                title='Help',
                exclude_from_nav=False,
            )

            if not items.get('action-item-help', False):
                action_folder = plone.api.content.create(
                    type='Folder',
                    container=items,
                    id='action-item-help',
                    title='Tasks Help',
                    exclude_from_nav=True,
                    layout='tabular_view',
                )


            wf_name = u'Tasks WF'
            if not action_folder.get(wf_name, False):
                wf_image = plone.api.content.create(
                        type='Image',
                        container=action_folder,
                        id='action-item-wf',
                        title=wf_name,
                        
                    )
                wf_image.image = load_image()

            
            if not action_folder.get('action-item-help', False):
                action_items = plone.api.content.create(
                    type='Document',
                    description=u'Tasks Help',
                    container=action_folder,
                    id='action-item-help',
                    title='Tasks Help',

                )

                pdf_name = u'Tasks Help'
                # if not action_folder.get(pdf_name, False):
                pdf_file = plone.api.content.create(
                            type='File',
                            container=action_folder,
                            id='ai-help.pdf',
                            title=pdf_name,
                            
                        )
                pdf_file.file = load_file()


            if not items.get('word-help', False):
                word_folder = plone.api.content.create(
                    type='Folder',
                    container=items,
                    id='word-help',
                    title='Word Help',
                    exclude_from_nav=True,
                    layout='tabular_view',
                )


                wf_name = u'Word WF'
                if not word_folder.get(wf_name, False):
                    wf_image = plone.api.content.create(
                            type='Image',
                            container=word_folder,
                            id='word-wf',
                            title=wf_name,
                            
                        )
                    wf_image.image = load_image()

                


                if not word_folder.get('word-help', False):
                    word = plone.api.content.create(
                        type='Document',
                        description=u'Word Help',
                        container=word_folder,
                        id='word-help',
                        title='Word Help',

                    )

            # if not items.get('scope-help', False):
            #     scope_folder = plone.api.content.create(
            #         type='Folder',
            #         container=items,
            #         id='scope-help',
            #         title='Scope Help',
            #         exclude_from_nav=True,
            #     )


            # wf_name = u'Scope WF'
            # if not scope_folder.get(wf_name, False):
            #     wf_image = plone.api.content.create(
            #             type='Image',
            #             container=scope_folder,
            #             id='scope-wf',
            #             title=wf_name,
                        
            #         )
            #     wf_image.image = load_image()

            


            # if not scope_folder.get('scope-help', False):
            #     scope = plone.api.content.create(
            #         type='Document',
            #         description=u'scope Help',
            #         container=scope_folder,
            #         id='scope-help',
            #         title='Scope Help',

            #     )

            
                
                
                
            
        if not portal.get('templates', False):
            templates_folder = plone.api.content.create(
                type='Folder',
                container=portal,
                id='templates',
                title='Templates',
                exclude_from_nav=True,
                layout='tabular_view',
            )
            
            wordfiles = [
                {'filetitle': 'main-template.docx.dot', 'filename': 'main-template.docx.dot'},
                {'filetitle': 'Meeting Agenda.docm', 'filename': 'Meeting_Agenda.docm'},
                {'filetitle': 'Meeting Minutes.docx', 'filename': 'Meeting_Minutes.docx'},
                {'filetitle': 'Meeting Notes.docm', 'filename': 'Meeting_Notes.docm'},
            ]
            
            for wordfile in wordfiles:
            
                file = plone.api.content.create(
                    type='File',
                    container=templates_folder,
                    title=wordfile['filetitle'],
                )
                file.file = load_word_file(wordfile['filename'])
                    
        if not portal.get('images', False):
            images_folder = plone.api.content.create(
                type='Folder',
                container=portal,
                id='images',
                title='Images',                 
                exclude_from_nav=True,
            )


        if not portal.get('downloads', False):
            downloads = plone.api.content.create(
                type='Folder',
                container=portal,
                id='downloads',
                title='Downloads',
                exclude_from_nav=True,
                layout='tabular_view',

            )

            if not downloads.get('board_president', False):
                project_manager = plone.api.content.create(
                    type='Folder',
                    container=downloads,
                    id='board_president',
                    title='Board President',
                    exclude_from_nav=True,
                    layout='tabular_view',
                )

            if not downloads.get('team_member', False):
                downloads = plone.api.content.create(
                    type='Folder',
                    container=downloads,
                    id='team_member',
                    title='Team Member',
                    exclude_from_nav=True,
                    layout='tabular_view',
                )


                
                



 

        if not portal.get('images', False):
            items = plone.api.content.create(
                type='Folder',
                container=portal,
                id='images',
                title='Images',
                exclude_from_nav=True,
            )

def uninstall(context):
    """Uninstall script"""
    # Do something at the end of the uninstallation of this package.

def load_image():
    filename = os.path.join(os.path.dirname(__file__), 'img', 'blank.png')
    with open(filename, 'rb') as image_file:
        return NamedBlobImage(
            data=image_file.read(),
            filename='dummy.png'
        )

def load_file():
    filename = os.path.join(os.path.dirname(__file__), 'pdf', 'ai-help.pdf')
    with open(filename, 'rb') as pdf_file:
        return NamedBlobFile(
            data=pdf_file.read(),
            filename='ai-help.pdf'
        )
     
def load_word_file(name):
    filename = os.path.join(os.path.dirname(__file__), 'word', name)
    with open(filename, 'rb') as word_file:
        return NamedBlobFile(
            data=word_file.read(),
            filename=name
        )

def _create_more_content(portal):        
    sitecollections = [
            {
            "@id": "site-collections/tasks-green", 
            "@type": "Collection", 
            "description": "Action items due more than 15 days from now",
            "query": [
                {
                "i": "portal_type", 
                "o": "plone.app.querystring.operation.selection.any", 
                "v": [
                    "action_items"
                ]
                }, 
                {
                "i": "duedate", 
                "o": "plone.app.querystring.operation.date.afterRelativeDate", 
                "v": "29"
                }, 
                {
                "i": "assigned_id", 
                "o": "plone.app.querystring.operation.string.currentUser", 
                "v": ""
                }, 
                {
                "i": "closed", 
                "o": "plone.app.querystring.operation.string.is", 
                "v": "No"
                }
            ], 
            "review_state": "published", 
            "title": "Tasks - Green", 
            "type_title": "Collection"
            }, 
            {
            "@id": "site-collections/tasks-red", 
            "@type": "Collection", 
            "description": "Critical Tasks",  
            "query": [
                {
                "i": "portal_type", 
                "o": "plone.app.querystring.operation.selection.any", 
                "v": [
                    "action_items"
                ]
                }, 
                {
                "i": "assigned_id", 
                "o": "plone.app.querystring.operation.string.currentUser", 
                "v": ""
                }, 
                {
                "i": "closed", 
                "o": "plone.app.querystring.operation.string.is", 
                "v": "No"
                }, 
                {
                "i": "priority", 
                "o": "plone.app.querystring.operation.int.is", 
                "v": "1"
                }
            ], 
            "review_state": "published", 
            "title": "Tasks - Red", 
            "type_title": "Collection"
            }, 
            {
            "@id": "site-collections/notifications-information", 
            "@type": "Collection", 
            "description": "All notifications classed as \"information\"",
            "query": [
                {
                "i": "portal_type", 
                "o": "plone.app.querystring.operation.selection.any", 
                "v": [
                    "Notification"
                ]
                }
            ], 
            "review_state": "published", 
            "title": "Notifications - Information", 
            "type_title": "Collection"
            }, 
            {
            "@id": "site-collections/notifications-important", 
            "@type": "Collection", 
            "description": "",
            "query": [
                {
                "i": "portal_type", 
                "o": "plone.app.querystring.operation.selection.any", 
                "v": [
                    "Notification"
                ]
                }
            ], 
            "review_state": "published", 
            "title": "Notifications - Important", 
            "type_title": "Collection"
            }, 
            {
            "@id": "site-collections/notifications-critical", 
            "@type": "Collection", 
            "description": "",
            "query": [
                {
                "i": "portal_type", 
                "o": "plone.app.querystring.operation.selection.any", 
                "v": [
                    "Notification"
                ]
                }
            ], 
            "review_state": "published", 
            "title": "Notifications - Critical", 
            "type_title": "Collection"
            }, 
            {
            "@id": "site-collections/tasks-yellow", 
            "@type": "Collection", 
            "description": "",
            "query": [
                {
                "i": "portal_type", 
                "o": "plone.app.querystring.operation.selection.any", 
                "v": [
                    "action_items"
                ]
                }, 
                {
                "i": "assigned_id", 
                "o": "plone.app.querystring.operation.string.currentUser", 
                "v": ""
                }, 
                {
                "i": "duedate", 
                "o": "plone.app.querystring.operation.date.afterRelativeDate", 
                "v": "6"
                }, 
                {
                "i": "duedate", 
                "o": "plone.app.querystring.operation.date.beforeRelativeDate", 
                "v": "16"
                }, 
                {
                "i": "closed", 
                "o": "plone.app.querystring.operation.string.is", 
                "v": "No"
                }
            ], 
            "review_state": "published", 
            "title": "Tasks - Yellow", 
            "type_title": "Collection"
            }, 
            {
            "@id": "action-items/action-items-collection", 
            "@type": "Collection", 
            "description": "",
            "query": [
                {
                "i": "portal_type", 
                "o": "plone.app.querystring.operation.selection.any", 
                "v": [
                    "action_items"
                ]
                }
            ], 
            "review_state": "published", 
            "title": "Action Items", 
            "type_title": "Collection"
            }, 
            {
            "@id": "postit_notes/postit-collection", 
            "@type": "Collection", 
            "description": "", 
            "query": [
                {
                "i": "portal_type", 
                "o": "plone.app.querystring.operation.selection.any", 
                "v": [
                    "postit_notes", 
                    "postit_note", 
                    "PostIt Notes"
                ]
                }, 
                {
                "i": "Creator", 
                "o": "plone.app.querystring.operation.string.currentUser", 
                "v": ""
                }
            ], 
            "review_state": "published", 
            "title": "Post It Notes", 
            "type_title": "Collection"
            }, 
            {
            "@id": "feedback/feedback-collection", 
            "@type": "Collection", 
            "description": "These are comments submitted by users of this website and Word Docent toolbar. The project manager should review all feedback items and respond if requested by the person submitting the Feedback", 
            "query": [
                {
                "i": "portal_type", 
                "o": "plone.app.querystring.operation.selection.any", 
                "v": [
                    "feedback"
                ]
                }
            ], 
            "review_state": "published", 
            "title": "Feedback", 
            "type_title": "Collection"
            }, 
            {
            "@id": "images/collection-of-all-site-images", 
            "@type": "Collection", 
            "description": "", 
            "query": [
                {
                "i": "portal_type", 
                "o": "plone.app.querystring.operation.selection.any", 
                "v": [
                    "Image"
                ]
                }
            ], 
            "review_state": "published", 
            "title": "Collection of All Site Images", 
            "type_title": "Collection"
            }, 
            {
            "@id": "site-collections/collection-of-collections", 
            "@type": "Collection", 
            "description": "This collects all the collections on the site.   This helps me keep track of the collections i have and where they are.  helps avoid duplication.", 
            "query": [
                {
                "i": "portal_type", 
                "o": "plone.app.querystring.operation.selection.any", 
                "v": [
                    "Collection"
                ]
                }, 
                {
                "i": "getId", 
                "o": "plone.app.querystring.operation.string.isNot", 
                "v": "collection-of-collections"
                }
            ], 
            "review_state": "published", 
            "title": "Collection of Collections", 
            "type_title": "Collection"
            }, 
            {
            "@id": "calendar/calendar", 
            "@type": "Collection", 
            "description": "", 
            "query": [
                {
                "i": "portal_type", 
                "o": "plone.app.querystring.operation.selection.any", 
                "v": [
                    "meeting"
                ]
                }
            ], 
            "review_state": "published", 
            "title": "Calendar", 
            "type_title": "Collection"
            }
        ] 
 
    
    for collection in sitecollections:  
        import pdb; pdb.set_trace() 
        my_id = collection['@id']
        my_folder = my_id.split('/')[0] 
        print(my_folder)
        if portal.get(my_folder, False):
            folder = portal.get(my_folder) 
        else:
            folder = plone.api.content.create(
                    type='Folder',
                    container=portal,
                    id=my_folder,
                    title=my_folder 
                )
                
        # if folder:  
        id = my_id.split('/')[1] 
        if not folder.get(id, False):           
            kollection  = plone.api.content.create(
                    type='Collection',
                    container=folder,
                    id=id,
                    title=collection['title'],
                    description = collection['description'],
                    query =  collection['query']
                )
                         

        
 


