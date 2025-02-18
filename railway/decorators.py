from django.conf import settings
from rest_framework.response import Response
from rest_framework import status
from functools import wraps

def admin_api_required(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        api_key = request.headers.get('API-KEY')
        if api_key != settings.ADMIN_API_KEY:
            return Response({"error": "Unauthorized: Invalid API key"}, status=status.HTTP_401_UNAUTHORIZED)
        return view_func(request, *args, **kwargs)
    return _wrapped_view
