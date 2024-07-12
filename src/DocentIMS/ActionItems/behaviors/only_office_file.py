# -*- coding: utf-8 -*-

from DocentIMS.ActionItems import _
from zope.component import adapter
from zope.interface import Interface
#from plone import schema
#from plone.autoform.interfaces import IFormFieldProvider
#from Products.CMFPlone.utils import safe_hasattr
#from zope.interface import implementer
#from zope.interface import provider

#from plone.autoform import directives

#>>> from zope.interface import Interface
#>>> from plone.namedfile import field
#>>> from plone.namedfile.interfaces import HAVE_BLOBS
#from plone.namedfile.field import NamedBlobFile

class IOnlyOfficeFileMarker(Interface):
    pass


# @provider(IFormFieldProvider)
#class IOnlyOfficeFile(model.Schema):
#     """
#     """

#     # file = NamedBlobFile(
#     #     title=_(u'File'),
#     #     description=_(u'File can be used with onlyoffice'),
#     #     required=False,
#     # )


#@implementer(IOnlyOfficeFile)
@adapter(IOnlyOfficeFileMarker)
class OnlyOfficeFile(object):
    def __init__(self, context):
        self.context = context

    # @property
    # def project(self):
    #     if safe_hasattr(self.context, 'file'):
    #         return self.context.file
    #     return None

    # @project.setter
    # def project(self, value):
    #     self.context.file = value
