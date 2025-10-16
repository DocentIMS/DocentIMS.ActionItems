from Products.PortalTransforms.interfaces import ITransform
from zope.interface import implementer
import markdown


# @implementer(ITransform)
# class QuarkToHTML:
#     __name__ = "quark_to_html"
#     inputs = ("text/x-web-markdown",)
#     output = "text/html"
    
#     import pdb; pdb.set_trace()

#     def name(self):
#         return self.__name__
    

#     def convert(self, orig, data, **kwargs):
#         return 'data'


# def register():
#     return QuarkToHTML()

  