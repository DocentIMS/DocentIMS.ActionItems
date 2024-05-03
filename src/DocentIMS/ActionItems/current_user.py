from zope.interface import provider
from zope.schema.interfaces import IContextAwareDefaultFactory
from plone import api

#@provider(IDefaultFactory)

@provider(IContextAwareDefaultFactory)
def getUserId(context):
    current_user = api.user.get_current()
    user_groups =  current_user.getGroups()
    if 'AuthenticatedUsers' in user_groups:
        return current_user.id
    return None



 