# from plone.app.textfield import RichText
# from plone.dexterity.interfaces import IDexterityContent
# from plone.app.discussion.interfaces import IComment
# from zope.component import adapter
# from zope.interface import Interface
# from plone.autoform.interfaces import IFormFieldProvider
# from plone.supermodel import model
# from zope.interface import implementer
# from DocentIMS.ActionItems.interfaces import IDocentimsActionitemsLayer
# from zope.interface import alsoProvides

# @implementer(IDocentimsActionitemsLayer)
# class ICustomCommentFields(model.Schema):
#     """Schema to override the comment field with RichText."""

#     text = RichText(
#         title=u"Comment",
#         required=True,
#     )

# # Declare this is a form field provider
# alsoProvides(ICustomCommentFields, IFormFieldProvider)
