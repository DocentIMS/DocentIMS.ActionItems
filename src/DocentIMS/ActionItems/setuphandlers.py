# -*- coding: utf-8 -*-
from Products.CMFPlone.interfaces import INonInstallable
from zope.interface import implementer
from plone import api


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
    if not portal.get('action_items', False):
        action_items = api.content.create(
                type='Folder',
                container=portal,
                id='action_items',
                title='Action Items',
            )

def uninstall(context):
    """Uninstall script"""
    # Do something at the end of the uninstallation of this package.
