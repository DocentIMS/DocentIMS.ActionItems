from Products.PortalTransforms.interfaces import ITransform
from zope.interface import implementer
from Products.PortalTransforms.libtransforms.commandtransform import popentransform


@implementer(ITransform)
class docx_to_text(popentransform):
    __name__ = "docx_to_text"
    inputs = ("application/vnd.openxmlformats-officedocument.wordprocessingml.document",)
    output = "text/plain"
    output_encoding = "utf-8"

    binaryName = "docx2txt"
    binaryArgs = "- -enc UTF-8 -"


def register():
    return docx_to_text()