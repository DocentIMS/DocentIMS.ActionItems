from zope.publisher.browser import BrowserView
from plone.dexterity.browser.add import DefaultAddView
from plone.dexterity.browser.add import DefaultAddForm
from plone.dexterity.browser.edit import DefaultEditView
from plone.dexterity.browser.edit import DefaultEditForm

class ActionItemsAddForm(DefaultAddForm):
    default_fieldset_label = 'Home'

class ActionItemsEditForm(DefaultEditForm):
    default_fieldset_label = 'Home'

class ActionItemsAddFormView(DefaultAddView):
    form = ActionItemsAddForm

class ActionItemsEditFormView(DefaultEditView):
    form = ActionItemsEditForm
