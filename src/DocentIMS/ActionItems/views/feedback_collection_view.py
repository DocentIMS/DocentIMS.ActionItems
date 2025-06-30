# -*- coding: utf-8 -*-

# from DocentIMS.ActionItems import _
from plone.app.contenttypes.browser.collection import CollectionView
from zope.interface import Interface

# from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile


class IFeedbackCollectionView(Interface):
    """ Marker Interface for IFeedbackCollectionView"""


class FeedbackCollectionView(CollectionView):
    # If you want to define a template here, please remove the template from
    # the configure.zcml registration of this view.
    # template = ViewPageTemplateFile('feedback_collection_view.pt')

    def __call__(self):
        # Implement your own actions:
        return super(FeedbackCollectionView, self).__call__()
