# -*- coding: utf-8 -*-
from Products.CMFPlone.interfaces import INonInstallable
from zope.interface import implementer
from plone import api

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
    _create_content(portal)

def _create_content(portal):
        action_items = api.content.create(
                type='Folder',
                container=portal,
                id='action_items',
                title='Action Items',

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
