from django import template
# В template.Library зарегистрированы все теги и фильтры шаблонов
# добавляем к ним и наш фильтр
from recipes.models import RecipeTag, TagChoices

register = template.Library()


@register.filter
def field_verbose_name(obj, field):
    return obj._meta.get_field(field).verbose_name.title()


@register.filter
def field_verbose_name_plural(obj, field):
    return obj._meta.get_field(field).verbose_name_plural.title()

from urllib.parse import urlencode
@register.filter
def obj_verbose_name(obj):
    return obj._meta.verbose_name

@register.filter
def obj_verbose_name_plural(obj):
    return obj._meta.verbose_name_plural


@register.filter
def int_format(obj):

    def digit_int_format(item):
        if type(item) == int:
            return item
        if type(item) == str:
            if not item.isdigit():
                return item
            return int(item)
        return item

    if type(obj) in (str, int):
        return digit_int_format(obj)

    if type(obj) == list:
        cp_obj = []
        for item in obj:
            print('obj', obj, 'add item', item)
            if type(item) not in (str, int):
                return obj
            print('added!')
            cp_obj.append(digit_int_format(item))
        return cp_obj

    return obj


@register.filter
def change_tag(obj, tag):
    all_tag_names = [name[0] for name in TagChoices.choices]

    print('tag: ', tag)
    curr_tags = obj.copy()
    # curr_tags = []
    # copy_tags = obj.copy()
    # for t in copy_tags:
    #     if t in all_tag_names:
    #         curr_tags.append(t)
    if tag in curr_tags:
        curr_tags.remove(tag)
    elif tag in all_tag_names:
        curr_tags.append(tag)
    params = urlencode({'tags': curr_tags}, doseq=True)
    print(params)
    # reply=''
    # for tag in curr_tags:
    #     reply += f'tags={tag}&'
    # reply = reply[:-1]
    # print(reply)
    return params