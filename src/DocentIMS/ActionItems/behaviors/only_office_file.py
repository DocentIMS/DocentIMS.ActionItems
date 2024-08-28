# -*- coding: utf-8 -*-

from DocentIMS.ActionItems import _
from zope.component import adapter
from zope.interface import Interface

class IOnlyOfficeFileMarker(Interface):
    pass



@adapter(IOnlyOfficeFileMarker)
class OnlyOfficeFile(object):
    def __init__(self, context):
        self.context = context
