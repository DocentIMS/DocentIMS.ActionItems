from Acquisition import aq_inner
from Acquisition import aq_parent
from plone.contentrules.engine.interfaces import IRuleExecutor
from plone.contentrules.engine.interfaces import IRuleStorage
from plone.contentrules.engine.interfaces import StopRule
from plone.uuid.interfaces import IUUID
from Products.CMFCore.interfaces import IContentish
from Products.CMFCore.interfaces import ISiteRoot
from zope.component import queryUtility
from zope.component.hooks import getSite

import threading


def _get_uid(context):
    uid = IUUID(context, None)
    if uid is not None:
        return uid

    try:
        return "/".join(context.getPhysicalPath())
    except AttributeError:
        pass

    try:
        return context.id
    except AttributeError:
        return ""




def user_logged_in_first(event):
    """When a user is logged in, execute rules assigned to the Plonesite."""
    execute_user_rules(event)

