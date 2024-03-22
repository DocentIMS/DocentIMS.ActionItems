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
    #import pdb; pdb.set_trace()
    #redirect(event)
    # import pdb; pdb.set_trace()
    execute_user_rules(event)
    
    
# def redirect(event):
#     #import pdb; pdb.set_trace()
#     request = event.object.REQUEST
#     #came_from = request.form.get('came_from', None)
#     came_from='vg.no'
#     if came_from:
#         response = request.RESPONSE
#         response.redirect(came_from)
    
    

