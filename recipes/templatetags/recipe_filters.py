from urllib.parse import urlencode
from django import template

from recipes.models import TagChoices

# В template.Library зарегистрированы все теги и фильтры шаблонов
register = template.Library()


def to_int_format(item):
    if isinstance(item, int):
        return item
    if isinstance(item, str) and item.isdigit():
        return int(item)
    return item


@register.filter
def field_verbose_name(obj, field):
    return obj._meta.get_field(field).verbose_name.title()


@register.filter
def field_verbose_name_plural(obj, field):
    return obj._meta.get_field(field).verbose_name_plural.title()


@register.filter
def obj_verbose_name(obj):
    return obj._meta.verbose_name


@register.filter
def obj_verbose_name_plural(obj):
    return obj._meta.verbose_name_plural


@register.filter
def change_tag(obj, tag):
    all_tag_names = [name[0] for name in TagChoices.choices]
    curr_tags = obj.copy()

    if tag in curr_tags:
        curr_tags.remove(tag)
    elif tag in all_tag_names:
        curr_tags.append(tag)
    params = urlencode({'tags': curr_tags}, doseq=True)
    return params


@register.filter
def top_slice(obj):
    return f':{obj}'


@register.filter
def int_format(obj):
    """
    Приводит текстовые цифры и списки цифр к числам.
    """
    if isinstance(obj, str) or isinstance(obj, int):
        return to_int_format(obj)

    if isinstance(obj, list):
        cp_obj = []
        for item in obj:
            if (not isinstance(item, str)) and (not isinstance(item, int)):
                return obj
            cp_obj.append(to_int_format(item))
        return cp_obj

    return obj


@register.filter
def sub(obj, arg):
    return to_int_format(obj) - to_int_format(arg)


@register.filter
def cyr_pluralize(obj, num):
    obj = to_int_format(obj)
    num = to_int_format(num)
    if type(num) != int or type(obj) != int:
        return 'ов'
    dig = str(obj - num)
    if dig[-1] == '1':
        return ''
    if dig[-1] in ['2', '3', '4']:
        return 'а'
    return 'ов'
