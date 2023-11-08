import re

from django import template

register = template.Library()


# Renvoie un séparateur de millier ' ' avec 2 décimales sous la forme 4 500,00
@register.filter('space_separator')
def space_separator(number):
    pattern = '(?<=\d)(?=(?:\d{3})+(?!\d))'
    repl = r" "
    string = str(number)
    result = re.sub(pattern, repl, string)
    return result
