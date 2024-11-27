from OFS.SimpleItem import SimpleItem
from plone.app.contentrules import PloneMessageFactory as _
from plone.app.contentrules.browser.formhelper import AddForm
from plone.app.contentrules.browser.formhelper import ContentRuleFormWrapper
from plone.app.contentrules.browser.formhelper import EditForm
from plone.contentrules.rule.interfaces import IExecutable
from plone.contentrules.rule.interfaces import IRuleElementData
from Products.CMFCore.Expression import createExprContext
from Products.CMFCore.Expression import Expression
from Products.CMFCore.utils import getToolByName
from z3c.form import form
from zope import schema
from plone.autoform import directives 
from zope.component import adapter
from zope.interface import implementer
from zope.interface import Interface
# from plone.supermodel import model
 
# from plone.app.z3cform.widgets.select import AjaxSelectFieldWidget

# subjects



class IFieldCondition(Interface):
    """Interface for the configurable aspects of a Field condition.

    This is also used to create add and edit forms, below.
    """
    
    field = schema.TextLine(
        title=_("label_field", default="Field"),
        description=_(
            "help_field",
            default="Name of field",
        ),
        required=True,
    )
    
    value = schema.TextLine(
        title=_("label_field_value", default="Field Value"),
        description=_(
            "help_field_value",
            default="Field value",
        ),
        required=True,
    )
    
 
@implementer(IFieldCondition, IRuleElementData)
class FieldCondition(SimpleItem):
    """The actual persistent implementation of the FieldS condition
    element.
    """

    field = ""
    element = "plone.conditions.Field"

    @property
    def summary(self):
        return _(
            "Field is: ${field}",
            mapping={"field": self.field},
        )


@implementer(IExecutable)
@adapter(Interface, IFieldCondition, Interface)
class FieldConditionExecutor:
    """The executor for this condition.

    This is registered as an adapter in configure.zcml
    """

    def __init__(self, context, element, event):
        self.context = context
        self.element = element
        self.event = event

    def __call__(self):
        object = self.event.object
        field = self.element.field
        value = self.element.value
        
        # Specify the field to check for  
        
        if field and value:
            attribute = getattr(object, field, None)
            field_type = type(attribute) if attribute is not None else None
            if field_type is not None:
                converted_value = field_type(value)
                if getattr(object, field, None) == converted_value:
                    return True
        
        return False
    


class FieldAddForm(AddForm):
    """An add form for tag expression condition."""

    schema = IFieldCondition
    label = _("Add Field Condition")
    description = _(
        "A Field condition makes the rule apply "
        "only if Field is not False in context."
    )
    form_name = _("Configure element")

    def create(self, data):
        c = FieldCondition()
        form.applyChanges(self, c, data)
        return c


class FieldAddFormView(ContentRuleFormWrapper):
    form = FieldAddForm


class FieldEditForm(EditForm):
    """An edit form for Field condition"""

    schema = IFieldCondition
    label = _("Edit Field Condition")
    description = _(
        "A Field condition makes the rule apply "
        "only if Field value is not False in context."
    )
    form_name = _("Configure element")


class FieldEditFormView(ContentRuleFormWrapper):
    form = FieldEditForm