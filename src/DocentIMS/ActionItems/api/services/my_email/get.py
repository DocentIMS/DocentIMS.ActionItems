# -*- coding: utf-8 -*-
from plone import api
from plone.restapi.interfaces import IExpandableElement
from plone.restapi.services import Service
from zope.component import adapter
from zope.interface import Interface
from zope.interface import implementer
from zExceptions import BadRequest


@implementer(IExpandableElement)
@adapter(Interface, Interface)
class MyEmail(object):

    def __init__(self, context, request):
        self.context = context.aq_explicit
        self.request = request

    def __call__(self, expand=False):
        result = {
            'my_email': {
                '@id': '{}/@my_email'.format(
                    self.context.absolute_url(),
                ),
            },
        }
        if not expand:
            return result

        # === Your custom code comes here ===

        user = api.user.get_current()   
        #import pdb; pdb.set_trace()
        #if api.user.is_anonymous():
        #usermail = self.request.get('email', None)
        #if not usermail:
        #    self.request.response.setStatus(401)
                
        #    user = api.user.get(username=usermail) 
            
        if not user:
                self.request.response.setStatus(401)
                
            
        if user:    
            result = {
                'my_email': {
                    'id': user.getProperty('id'),
                    'email': user.getProperty('email'),
                    'fullname' : user.getProperty('fullname'),         
                },
            }
            
            return result
        
        self.request.response.setStatus(401)


class MyEmailGet(Service):

    def reply(self):
        #if api.user.is_anonymous():
        #    raise BadRequest("Parameters supplied are not valid")
        #    # self.request.response.setStatus(401)
        service_factory = MyEmail(self.context, self.request)
        return service_factory(expand=True)['my_email']
