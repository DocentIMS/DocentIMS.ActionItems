from OFS.SimpleItem import SimpleItem
from plone.app.contentrules import PloneMessageFactory as _
from plone.app.contentrules.actions import ActionAddForm
from plone.app.contentrules.actions import ActionEditForm

from plone.app.contentrules.browser.formhelper import ContentRuleFormWrapper
from plone.contentrules.rule.interfaces import IExecutable
from plone.contentrules.rule.interfaces import IRuleElementData
from Products.statusmessages.interfaces import IStatusMessage
from zope import schema
from zope.component import adapter
from zope.interface import implementer
from zope.interface import Interface



 



class ILogginFirstAction(Interface):
    """Interface for the configurable aspects of a FirstLoggedin action.

    This is also used to create add and edit forms, below.
    """

    message = schema.TextLine(
        title=_("Page to redirect to"),
        description=_("Where to send logged in users."),
        required=True,
    )




@implementer(ILogginFirstAction, IRuleElementData)
class LogginFirstAction(SimpleItem):
    """The actual persistent implementation of the FirstLoggedin action element."""

    message = ""
    message_type = "info"
    
    element = "DocentIMS.ActionItems.LogginFirst"
    
    #Redirect user here

    @property
    def summary(self):
        return _(
            "FirstLoggedin with message ${message}",
            mapping=dict(message=self.message),
        )


@adapter(Interface, ILogginFirstAction, Interface)
@implementer(IExecutable)
class LogginFirstActionExecutor:
    """The executor for this action.

    This is registered as an adapter in configure.zcml
    """

    def __init__(self, context, element, event):
        self.context = context
        self.element = element
        self.event = event

    def __call__(self):
        request = self.context.REQUEST
        message = _(self.element.message)
        message_type = self.element.message_type
        # request.response.redirect('came_from')
        IStatusMessage(request).addStatusMessage(message, type=message_type)
        # To do
        #request = self.REQUEST
        
        return True


class LogginFirstAddForm(ActionAddForm):
    """An add form for FirstLoggedin rule actions."""

    schema = ILogginFirstAction
    label = _("Add FirstLoggedin Action")
    description = _("A FirstLoggedin action can show a message to the user.")
    form_name = _("Configure element")
    Type = LogginFirstAction


class LogginFirstAddFormView(ContentRuleFormWrapper):
    form = LogginFirstAddForm


class LogginFirstEditForm(ActionEditForm):
    """An edit form for FirstLoggedin rule actions.

    z3c.form does all the magic here.
    """

    schema = ILogginFirstAction
    label = _("Edit FirstLoggedin Action")
    description = _("A FirstLoggedin action can show a message to the user.")
    form_name = _("Configure element")


class LogginFirstEditFormView(ContentRuleFormWrapper):
    form = LogginFirstAddForm