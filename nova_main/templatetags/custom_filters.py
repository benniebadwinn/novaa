# custom_filters.py

from django import template

register = template.Library()

@register.filter(name='format_with_commas')
def format_with_commas(value):
    """
    Add commas to a number for better readability.
    """
    try:
        value = float(value)
        value = "{:,.2f}".format(value)  # Format the number with commas and two decimal places
    except (TypeError, ValueError):
        pass
    return value
