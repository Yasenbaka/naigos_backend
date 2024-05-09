import json

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods


# Create your views here.

@require_http_methods(['POST'])
@csrf_exempt
def register_user(request):
    print(request.POST.get('appid'))
    return JsonResponse({'status': 'success'})

