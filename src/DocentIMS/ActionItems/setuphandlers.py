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


        if not portal.get('action_items', False):
            action_items = plone.api.content.create(
                type='Folder',
                container=portal,
                id='action_items',
                title='Action Items',
                layout='action-overview'

            )


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



        if not portal.get('scope-analysis', False):
            action_items = plone.api.content.create(
                type='Folder',
                Description=u'This folder holds the parsed files from the DocentIMS Word program.  These were used to create new instances of Scope Analysis',
                container=portal,
                id='scope-analysis',
                title='Scope Analysis',
                layout='sow-overview',

            )

        if not portal.get('help_files', False):
            items = plone.api.content.create(
                type='Folder',
                container=portal,
                id='help_files',
                title='Help Files',
                exclude_from_nav=True,
            )

            wf_name = u'help.png'
            if not items.get(wf_name, False):
                wf_image = plone.api.content.create(
                        type='Image',
                        container=action_items,
                        id=wf_name,
                        title=wf_name,
                        
                    )
                wf_image.image = load_image()

    


            if not items.get('actionitemhelp', False):
                action_items = plone.api.content.create(
                    type='Document',
                    Description=u'Action Item Help',
                    container=action_items,
                    id='actionitemhelp',
                    title='Action Item Help',

                )



        


            #    behaviour = constrains.ISelectableConstra
        #import pdb; pdb.set_trace();
        #constrains.ISelectableConstrainTypes
        #constrains.ISelectableConstrainTypes
        #constrains.ISelectableConstrainTypes().setConstrainTypesMode(1)
        #self = portal
        #context = self.context
        #context = action_items
        #action_items.setLocallyAllowedTypes(["action_items"])
        #ConstrainTypesBehavior.setLocallyAllowedTypes(portal,  ['action_items'])
        #ConstrainTypesBehavior.getLocallyAllowedTypes(action_items)
        #ConstrainTypesBehavior.allowedContentTypes(portal)
        #ConstrainTypesBehavior.getImmediatelyAddableTypes(portal, context=action_items)
        #from plone.app.dexterity.behaviors.constrains import ConstrainTypesBehavior as behavior
        #action_items.allowed_content_types
        #action_items.allowedContentTypes = ['action_items']
        #constrains.ConstrainTypesBehavior.setImmediatelyAddableTypes(action_items, 'action_items' )
        #behavior.getConstrainTypeMode()
        #behavior = constrains.ISelectableConstrainsTypes(action_items)
        #behavior =  ISelectableConstrainsTypes(action_items)
        #setImmediatelyAddableType
        #behavior = setConstrainsTypesMode(constrains.ENABLED)
        #action_items.setConstrainTypesMode(constraintypes.ENABLED)
        #action_items.set  action_items.LocallyAllowedTypes =  ['action_items'],
        #action_items.setImmediatelyAddableTypes = ['action_items']

def uninstall(context):
    """Uninstall script"""
    # Do something at the end of the uninstallation of this package.


def load_image():
    filename = os.path.join(os.path.dirname(__file__), 'img', 'blank.png')
    with open(filename, 'rb') as image_file:
        return NamedBlobImage(
            data=image_file.read(),
            filename='blank.png'
        )