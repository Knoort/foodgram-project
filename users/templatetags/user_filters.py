from django import template
# В template.Library зарегистрированы все теги и фильтры шаблонов
# добавляем к ним и наш фильтр
register = template.Library()


@register.filter 
def addclass(field, css):
        return field.as_widget(attrs={"class": css})


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