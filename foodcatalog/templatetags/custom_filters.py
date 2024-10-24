# myapp/templatetags/custom_filters.py
from django import template

register = template.Library()

@register.filter
def safe_recipe_name(recipe_name):
    return recipe_name.replace('/', '@')  # Replace slashes with hyphens
