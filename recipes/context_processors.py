from .models import RecipeTag
from .utils import get_purchases

from urllib.parse import urlencode


def tags(request):
    all_tags = RecipeTag.objects.all()
    tags_checked = request.GET.getlist('tags', [])
    for tag in all_tags:
        link_get_params = tags_checked.copy()
        if tag.name in link_get_params:
            link_get_params.remove(tag.name)
        else:
            link_get_params.append(tag.name)
        tag.link = urlencode({'tags': link_get_params}, doseq=True)
        tag.checked = True if tag.name in tags_checked else False

    tags = {
        'all': all_tags,
        'checked': tags_checked,
        'checked_get_params': urlencode({'tags': tags_checked}, doseq=True)
    }
    return {'tags': tags}


def purchases_count(request):
    return {'purchases_count': get_purchases(request).count()}
