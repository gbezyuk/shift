"""
Template filters for update cart form
"""
from django import template
from django.forms.forms import BoundField

register = template.Library()

@register.filter(name='cart_form_remove_item_input')
def cart_form_remove_item_input(form, item_id):
    """
    Remove item input bound field filter
    """
    field_name = 'remove_item[%d]' % (item_id,)
    return BoundField(form, form.fields[field_name], field_name)

@register.filter(name='cart_form_item_quantity_input')
def cart_form_item_quantity_input(form, item_id):
    """
    Item quantity input bound field filter
    """
    field_name = 'item_quantity[%d]' % (item_id,)
    return BoundField(form, form.fields[field_name], field_name)