from .models import RecipeTag
from .utils import get_purchases


def tags(request):
    tags = {
        'all': RecipeTag.objects.all(),
        'checked': request.GET.getlist('tags', [])
    }
    return {'tags': tags}


def purchases_count(request):
    return {'purchases_count': get_purchases(request).count()}
