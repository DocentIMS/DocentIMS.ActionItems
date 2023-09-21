# -*- coding: utf-8 -*-
from Products.CMFPlone.interfaces import INonInstallable
from zope.interface import implementer
from plone import api
import os
from plone.namedfile.file import NamedBlobImage

from plone.base.interfaces import constrains
from plone.base.interfaces.constrains import IConstrainTypes
from plone.base.interfaces.constrains import ISelectableConstrainTypes

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

    # Create Folder to put everything in

    portal = api.portal.get()
    #api.portal.set_registry_record('DocentIMS.ActionItems.interfaces.IDocentimsSettings.table_columns', [{'row_field': 'actionno', 'row_title': 'ID'}, {'row_field': 'title', 'row_title': 'Title'}])
    _create_content(portal)

def _create_content(portal):
        if not portal.get('action_items', False):
            action_items = api.content.create(
                type='Folder',
                container=portal,
                id='action_items',
                title='Action Items',

            )

        if not portal.get('scope-analysis', False):
            action_items = api.content.create(
                type='Folder',
                Description=u'This folder holds the parsed files from the DocentIMS Word program.  These were used to create new instances of Scope Analysis',
                container=portal,
                id='scope-analysis',
                title='Scope Analysis',

            )

        wf_name = u'blank.png'
        wf_image = api.content.create(
                type='Image',
                container=portal,
                id=wf_name,
                title=wf_name,
                description=u'EMN 2012-2013'
            )
        wf_image.image = load_image()

 


        if not portal.get('actionitemhelp', False):
            action_items = api.content.create(
                type='Document',
                Description=u'Action Item Help',
                container=portal,
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