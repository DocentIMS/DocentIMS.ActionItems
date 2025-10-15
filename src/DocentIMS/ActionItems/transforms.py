from Products.PortalTransforms.interfaces import ITransform
from zope.interface import implementer
import markdown
from zope.interface import Interface



from plone.base.interfaces import IMarkupSchema
from plone.base.utils import safe_text
from plone.registry.interfaces import IRegistry
from Products.PortalTransforms.interfaces import ITransform
from Products.PortalTransforms.utils import log
from zope.component import getUtility
from zope.interface import implementer
from Products.PortalTransforms.libtransforms.commandtransform import commandtransform

@implementer(ITransform)
class quark(commandtransform):
    __name__ = "quark_to_html"
    inputs = ("text/x-web-markdown",)
    output = "text/html"
    
    binaryName = "rtf-converter"

    def __init__(self):
        commandtransform.__init__(self, binary=self.binaryName)


    def name(self):
        return self.__name__
    

    def convert(self, orig, data, **kwargs):
        return 'data'


def register():
    return quark()

 