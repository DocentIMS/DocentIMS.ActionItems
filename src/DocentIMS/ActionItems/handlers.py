#from Acquisition import aq_inner
#from Acquisition import aq_parent
#from plone.uuid.interfaces import IUUID
#from Products.CMFCore.interfaces import IContentish
#from Products.CMFCore.interfaces import ISiteRoot
#from zope.component import queryUtility
#from zope.component.hooks import getSite
from plone.app.contentrules.handlers  import execute_user_rules

def user_logged_in_first(event):
    """When a user is logged in first time, execute rules assigned to the Plonesite."""
    execute_user_rules(event)

