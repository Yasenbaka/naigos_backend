from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods

from api.models import SogouInputTheme


@require_http_methods(['GET'])
@csrf_exempt
def get_only_sogou_theme(request):
    theme_id = request.GET.get('theme_id')
    try:
        theme = SogouInputTheme.objects.get(theme_id=theme_id)
    except SogouInputTheme.DoesNotExist:
        return JsonResponse({
            'code': 1,
            'message': 'ID没有找到数据！'
        })
    return JsonResponse({
        'code': 0,
        'message': '获取数据！',
        'data': {
            'theme_id': theme.theme_id,
            'name': theme.name,
            'introduce': theme.introduce,
            'url': theme.url,
            'header_image': theme.header_image,
            'eject_image': theme.eject_image,
            'details_image': theme.details_image,
            'cost': theme.cost
        }
    })


@require_http_methods(['GET'])
@csrf_exempt
def get_all_sogou_themes(request):
    theme = SogouInputTheme.objects.all()
    themes_list = [
        {'theme_id': theme.theme_id,
         'name': theme.name,
         'header_image': theme.header_image,
         'eject_image': theme.eject_image
         }
        for theme in theme
    ]
    return JsonResponse({
        'code': 0,
        'message': '获取数据！',
        'data': themes_list
    })
