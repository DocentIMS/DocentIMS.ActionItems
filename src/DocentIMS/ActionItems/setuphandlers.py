# -*- coding: utf-8 -*-
from Products.CMFPlone.interfaces import INonInstallable
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
    
    #Set control panel properties, since we can not set them TTW
    #TODO: Maybe make a check 
    plone.api.portal.set_registry_record('DocentIMS.ActionItems.interfaces.IDocentimsSettings.table_columns', [{'row_field': 'actionno', 'row_title': 'ID'}, {'row_field': 'title', 'row_title': 'Title'}])
    plone.api.portal.set_registry_record('DocentIMS.ActionItems.interfaces.IDocentimsSettings.scope_table_columns',  [{'row_field': 'id', 'row_title': 'ID'}, {'row_field': 'title', 'row_title': 'Title'}])
    
    # Create Folder to put everything in
    _create_content(portal)



def post_import(context):
    """Post install script"""
    # Do something at the end of the installation of this package.

    
    portal = plone.api.portal.get()
    
    #Set control panel properties, since we can not set them TTW
    #TODO: Maybe make a check 
    plone.api.portal.set_registry_record('DocentIMS.ActionItems.interfaces.IDocentimsSettings.table_columns', [{'row_field': 'actionno', 'row_title': 'ID'}, {'row_field': 'title', 'row_title': 'Title'}])
    plone.api.portal.set_registry_record('DocentIMS.ActionItems.interfaces.IDocentimsSettings.scope_table_columns',  [{'row_field': 'id', 'row_title': 'ID'}, {'row_field': 'title', 'row_title': 'Title'}])
    
    # Create Folder to put everything in
    _create_content(portal)


def _create_content(portal):
        
        folderpath = os.path.dirname(__file__)
        fullpath = "{folderpath}/ai_import.xlsx".format(folderpath=folderpath)


        if not portal.get('action-items', False):
            action_items = plone.api.content.create(
                type='Folder',
                container=portal,
                id='action-items',
                title='Action Items',
                layout='action-overview',
                default_page='action-items-collection'

            )

            ## add collection inside here

            if not action_items.get('action-items-collection', False):
                action_items_collection = plone.api.content.create(
                    type='Collection',
                    container=action_items,
                    id='action-items-collection',
                    title='Action Items',
                    layout='action-overview'

                )


            try:
                df = pd.read_excel( fullpath )
                print(df)

                my_dict = df.to_dict(orient='index')

                for i in range(0, len(my_dict)):
                    print(my_dict[i])
                    title = my_dict[i].get('Title')
                    myid = "action_items-{id}".format(id=my_dict[i].get('ID'))
                    date = my_dict[i].get('Start')
                    #import pdb; pdb.set_trace()
                    date_time_obj =  datetime.datetime.strptime(str(date), '%Y-%m-%d %H:%M:%S')

                    initial_due_date = my_dict[i].get('Finish')
                    initial_due_date_time_obj =  datetime.datetime.strptime(str(initial_due_date), '%Y-%m-%d %H:%M:%S')

                    texte = my_dict[i].get('Predecessors')
                    notes = my_dict[i].get('Notes')
                    bodytext = txt1 = "{texte}<(br/> {notes}".format(texte = texte, notes = notes)
                    # texte + notes

                    action_item = plone.api.content.create(
                                type='action_items',
                                id=myid,
                                container=action_items,
                                title=title,
                                date=date_time_obj,
                                initial_due_date=initial_due_date_time_obj.date(),
                                priority = str((i%3) + 1)    
                    )

                    # count them ?

            except FileNotFoundError:
                pass



        if not portal.get('scope-analysis', False):
            action_items = plone.api.content.create(
                type='Folder',
                Description=u'This folder holds the parsed files from the DocentIMS Word program.  These were used to create new instances of Scope Analysis',
                container=portal,
                id='scope-analysis',
                title='Scope Analysis',
                layout='scope-overview',
                default_page='sow_collection'

            )

            ## add collection inside here

            action_items_collection = plone.api.content.create(
                type='Collection',
                container=action_items,
                id='sow-collection',
                title='Scope Analysis',
                layout='scope-overview'

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