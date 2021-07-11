from django import template
from django.contrib.auth.models import Group

register = template.Library()


@register.filter
def addclass(field, css):
    return field.as_widget(attrs={"class": css})


@register.filter(name='has_group')
def has_group(user, group_name):
    try:
        group = Group.objects.get(name=group_name)
        print(f'{user} group:', group)
    except:
        return False  # group doesn't exist, so for sure the user isn't part of the group

    # for superuser or staff, always return True
    if user.is_superuser:
        return True

    return user.groups.filter(name=group_name).exists()