# -*- coding: utf-8 -*-
from Products.CMFPlone.interfaces import INonInstallable
from Products.CMFCore.utils import getToolByName
from zope.interface import implementer
#from plone import api
import os
from plone.namedfile.file import NamedBlobImage

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
    
    #Assign role to Group 'Project Manager'
    plone.api.group.grant_roles(groupname='PrjMgr', roles=['Project Manager'])

    
    #Set control panel properties, since we can not set them TTW
    #TODO: Maybe make a check 
    plone.api.portal.set_registry_record('DocentIMS.ActionItems.interfaces.IDocentimsSettings.table_columns', 
                                         [{'row_field': 'title', 'row_title': 'Title'},
                                          {'row_field': 'assigned_to', 'row_title': 'Responsible person'},
                                          {'row_field': 'description', 'row_title': 'Description'},
                                          {'row_field': 'priority', 'row_title': 'Priority'},
                                          {'row_field': 'initial_due_date', 'row_title': 'Due date'},
                                         ])
    
    plone.api.portal.set_registry_record('DocentIMS.ActionItems.interfaces.IDocentimsSettings.scope_table_columns',
                                         [{'row_field': 'id', 'row_title': 'ID'}, 
                                          {'row_field': 'title', 'row_title': 'Title'},
                                          {'row_field': 'initial_due_date', 'row_title': 'Due date'},
                                          {'row_field': 'section_number', 'row_title': 'SN'},
                                          {'row_field': 'estimated_qc_time', 'row_title': 'QC time'}, 
                                          ])
    
    plone.api.portal.set_registry_record('DocentIMS.ActionItems.interfaces.IDocentimsSettings.vokabularies',
                                        [{'vocabulary_entry': 'Specialist'},
                                         {'vocabulary_entry': 'Coordinator'},
                                         {'vocabulary_entry': 'Teamworker'},
                                        ])
                                        
    plone.api.portal.set_registry_record('DocentIMS.ActionItems.interfaces.IDocentimsSettings.companies',
                                        [{'full_company_name': 'Docent IMS LLC',
                                          'short_company_name': 'Docent' ,
                                          'company_letter_kode': 'DOC',
                                          'company_role': '???',
                                          'company_full_street_address': '6317 157th place ne',
                                          'company_other_address': '',
                                          'company_city': 'Redmond',
                                          'company_state': 'WA',
                                          'company_zip': '98052'}
                                        ])
                                          
                                          
    # Create Folder to put everything in
    _create_content(portal)
    if not portal.get('frontpage', False):
        fpage = plone.api.content.create(
        type='FrontPage',
        container=portal,
        id='frontpage',
        title='Front page' 
    )
        
    portal.default_page='frontpage'
    
    #Restrict content types that can be added to folders
    action_folder = portal.get('action-items', False)
    behaviour = constrains.ISelectableConstrainTypes(action_folder)
    behaviour.setConstrainTypesMode(constrains.ENABLED)
    behaviour.setImmediatelyAddableTypes(['action_items'])
    behaviour.setLocallyAllowedTypes(['action_items'])

    scope_analysis = portal.get('scope-analysis', False)
    behaviour = constrains.ISelectableConstrainTypes(scope_analysis)
    behaviour.setConstrainTypesMode(constrains.ENABLED)
    behaviour.setImmediatelyAddableTypes(['sow_analysis'])
    behaviour.setLocallyAllowedTypes(['sow_analysis'])
    
    notes = portal.get('notes', False)
    behaviour = constrains.ISelectableConstrainTypes(notes)
    behaviour.setConstrainTypesMode(constrains.ENABLED)
    behaviour.setImmediatelyAddableTypes(['Notes'])
    behaviour.setLocallyAllowedTypes(['Notes'])
    
    feedback = portal.get('feedback', False)
    behaviour = constrains.ISelectableConstrainTypes(feedback)
    behaviour.setConstrainTypesMode(constrains.ENABLED)
    behaviour.setImmediatelyAddableTypes(['Feedback'])
    behaviour.setLocallyAllowedTypes(['Feedback'])

    meeting = portal.get('meeting', False)
    behaviour = constrains.ISelectableConstrainTypes(meeting)
    behaviour.setConstrainTypesMode(constrains.ENABLED)
    behaviour.setImmediatelyAddableTypes(['Meeting'])
    behaviour.setLocallyAllowedTypes(['Meeting'])

def pre_install(context):
    """Pre install script"""
    # Do something before the installation of this package.
    portal = plone.api.portal.get()
    
    #create groups, wayne might need these for workflow
    plone.api.group.create(groupname="PrjCust", title="Project Customer", description="The customer for the project")
    plone.api.group.create(groupname="PrjMgr", title="Project Manager", description="Person managing the project")
    plone.api.group.create(groupname="PrjTeam", title="Project Team", description="All Members of the Project")
    plone.api.group.create(groupname="PrjQcMgr", title="Project QC Manager", description="Person in charge of manage QC for the project")
   
    #create content 
    _create_content(portal)


def post_import(context):
    """Post install script"""
    # Do something at the end of the installation of this package.
    
    portal = plone.api.portal.get()
    
    #Set control panel properties, since we can not set them TTW
    #TODO: Maybe make a check 
    plone.api.portal.set_registry_record('DocentIMS.ActionItems.interfaces.IDocentimsSettings.table_columns', [{'row_field': 'actionno', 'row_title': 'ID'}, {'row_field': 'title', 'row_title': 'Title'}])
    plone.api.portal.set_registry_record('DocentIMS.ActionItems.interfaces.IDocentimsSettings.scope_table_columns',  [{'row_field': 'id', 'row_title': 'ID'}, {'row_field': 'title', 'row_title': 'Title'}])
    

    #Import excel content    
    _import_content(portal)
    

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
            
        if not portal.get('templates', False):
            images_folder = plone.api.content.create(
                type='Folder',
                container=portal,
                id='templates',
                title='Templates',
                exclude_from_nav=True,
            )
                    
        if not portal.get('images', False):
            images_folder = plone.api.content.create(
                type='Folder',
                container=portal,
                id='images',
                title='Images' 
            )


        if not portal.get('downloads', False):
            downloads = plone.api.content.create(
                type='Folder',
                container=portal,
                id='downloads',
                title='Downloads',
                exclude_from_nav=True,

            )

            if not downloads.get('project_manager', False):
                project_manager = plone.api.content.create(
                    type='Folder',
                    container=downloads,
                    id='project_manager',
                    title='Project Manager',
                    exclude_from_nav=True,
                )

            if not downloads.get('team_member', False):
                downloads = plone.api.content.create(
                    type='Folder',
                    container=downloads,
                    id='team_member',
                    title='Team Member',
                    exclude_from_nav=True,
                )


        if not portal.get('action-items', False):
            action_items = plone.api.content.create(
                type='Folder',
                container=portal,
                id='action-items',
                title='Action Items',
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
                    title='Action Items',
                    layout='action-overview',
                    query = [{'i': 'portal_type', 'o': 'plone.app.querystring.operation.selection.any', 'v': ['action_items']}],
                    limit=2000,
                    item_count=500,
                )
                
                
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
                    layout='tabular_view',
                    limit=2000,
                    item_count=500,
                    customViewFields = ['Title', 'Creator', 'CreationDate'],
                    query = [{'i': 'portal_type', 'o': 'plone.app.querystring.operation.selection.any', 'v': ['Feedback']}]
                )
            
        if not portal.get('meeting', False):
            meeting = plone.api.content.create(
                type='Folder',
                container=portal,
                id='meeting',
                title='Meetings',
                default_page='meeting-collection',
                nextPreviousEnabled=1
            )
            
            ## add collection inside
            
            if not meeting.get('meeting-collection', False):
                meeting_collection = plone.api.content.create(
                    type='Collection',
                    container=meeting,
                    id='meeting-collection',
                    title='Meetings',
                    query = [{'i': 'portal_type', 'o': 'plone.app.querystring.operation.selection.any', 'v': ['Meeting']}]
                )
                
        if not portal.get('notes', False):
            notes = plone.api.content.create(
                type='Folder',
                container=portal,
                id='notes',
                title='Notes',
                default_page='notes-collection',
                nextPreviousEnabled=1
            )
            
            ## add collection inside
            
            

            if not notes.get('notes-collection', False):
                notes_collection = plone.api.content.create(
                    type='Collection',
                    container=notes,
                    id='notes-collection',
                    title='Notes',
                    layout='tabular_view',
                    limit=2000,
                    item_count=500,
                    customViewFields = ['Title', 'CreationDate'],
                    query = [{'i': 'portal_type', 'o': 'plone.app.querystring.operation.selection.any', 'v': ['Notes']}]
                )
            


            # This is for importing dummy content, will require action items to be present (installed)
            # Dont remove, keep the code in case we need to install dummy content
            
            # try:
            #     df = pd.read_excel( fullpath )
            #     print(df)

            #     my_dict = df.to_dict(orient='index')

            #     for i in range(0, len(my_dict)):
            #         print(my_dict[i])
            #         title = my_dict[i].get('Title')
            #         myid = "action_items-{id}".format(id=my_dict[i].get('ID'))
            #         date = my_dict[i].get('Start')
            #         date_time_obj =  datetime.datetime.strptime(str(date), '%Y-%m-%d %H:%M:%S')

            #         initial_due_date = my_dict[i].get('Finish')
            #         initial_due_date_time_obj =  datetime.datetime.strptime(str(initial_due_date), '%Y-%m-%d %H:%M:%S')

            #         texte = my_dict[i].get('Predecessors')
            #         notes = my_dict[i].get('Notes')
            #         bodytext = txt1 = "{texte}<(br/> {notes}".format(texte = texte, notes = notes)
            #         action_item = plone.api.content.create(
            #                     type='action_items',
            #                     id=myid,
            #                     container=action_items,
            #                     title=title,
            #                     date=date_time_obj,
            #                     initial_due_date=initial_due_date_time_obj.date(),
            #                     priority = str((i%3) + 1)    
            #         )

                    
            # except FileNotFoundError:
            #     pass


        
        if not portal.get('scope-analysis', False):
            scopeanalysis = plone.api.content.create(
                type='Folder',
                container=portal,
                id='scope-analysis',
                title='Scope Breakdown',
                default_page='sow-collection',
                nextPreviousEnabled=1

            )
            
            # Description=u'This folder holds the parsed files from the DocentIMS Word program.  These were used to create new instances of Scope Analysis',
            ## add collection inside here

            scopeoverview = plone.api.content.create(
                type='Collection',
                container=scopeanalysis,
                id='sow-collection',
                title='Scope Breakdown',
                layout='sow-overview',
                query = [{'i': 'portal_type', 'o': 'plone.app.querystring.operation.selection.any', 'v': ['sow_analysis']}],
                limit=2000,
                item_count=500,
            )


        if not portal.get('images', False):
            items = plone.api.content.create(
                type='Folder',
                container=portal,
                id='images',
                title='Images',
                exclude_from_nav=True,
            )
        
        if not portal.get('help-files', False):
            items = plone.api.content.create(
                type='Folder',
                container=portal,
                id='help-files',
                title='Help Files',
                exclude_from_nav=True,
            )

            if not items.get('action-item-help', False):
                action_folder = plone.api.content.create(
                    type='Folder',
                    container=items,
                    id='action-item-help',
                    title='Action Item Help',
                    exclude_from_nav=True,
                )


            wf_name = u'Action Item WF'
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
                    Description=u'Action Item Help',
                    container=action_folder,
                    id='action-item-help',
                    title='Action Item Help',

                )


            if not items.get('word-help', False):
                word_folder = plone.api.content.create(
                    type='Folder',
                    container=items,
                    id='word-help',
                    title='Word Help',
                    exclude_from_nav=True,
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
                        Description=u'Word Help',
                        container=word_folder,
                        id='word-help',
                        title='Word Help',

                    )

            if not items.get('scope-help', False):
                scope_folder = plone.api.content.create(
                    type='Folder',
                    container=items,
                    id='scope-help',
                    title='Scope Help',
                    exclude_from_nav=True,
                )


            wf_name = u'Scope WF'
            if not scope_folder.get(wf_name, False):
                wf_image = plone.api.content.create(
                        type='Image',
                        container=scope_folder,
                        id='scope-wf',
                        title=wf_name,
                        
                    )
                wf_image.image = load_image()

            


            if not scope_folder.get('scope-help', False):
                scope = plone.api.content.create(
                    type='Document',
                    Description=u'scope Help',
                    container=scope_folder,
                    id='scope-help',
                    title='Scope Help',

                )

            
        # if not portal.get('frontpage', False):
        #     fpage = plone.api.content.create(
        #         type='FrontPage',
        #         container=portal,
        #         id='frontpage',
        #         title='Front page' 
        #     )


 

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





def _import_content(portal):

    folderpath = os.path.dirname(__file__)
    fullpath = "{folderpath}/ai_import.xlsx".format(folderpath=folderpath)
    action_items = plone.api.content.get(path='action-items')

    # This is for importing dummy content, will require action items to be present (installed)
    # Dont remove, keep the code in case we need to install dummy content
    
    try:
        df = pd.read_excel( fullpath )
        print(df)

        my_dict = df.to_dict(orient='index')

        for i in range(0, len(my_dict)):
            print(my_dict[i])
            title = my_dict[i].get('Title')
            myid = "action_items-{id}".format(id=my_dict[i].get('ID'))
            date = my_dict[i].get('Start')
            date_time_obj =  datetime.datetime.strptime(str(date), '%Y-%m-%d %H:%M:%S')

            initial_due_date = my_dict[i].get('Finish')
            initial_due_date_time_obj =  datetime.datetime.strptime(str(initial_due_date), '%Y-%m-%d %H:%M:%S')

            texte = my_dict[i].get('Predecessors')
            notes = my_dict[i].get('Notes')
            bodytext = txt1 = "{texte}<(br/> {notes}".format(texte = texte, notes = notes)
            action_item = plone.api.content.create(
                        type='action_items',
                        id=myid,
                        container=action_items,
                        title=title,
                        date=date_time_obj,
                        initial_due_date=initial_due_date_time_obj.date(),
                        priority = str((i%3) + 1)    
            )

            
    except FileNotFoundError:
        pass



    
