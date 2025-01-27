import json
from django.contrib.auth.models import User
from .models import Door, Permission, Log
from django.http import HttpRequest, HttpResponse, JsonResponse
from django.contrib.auth import authenticate, login, logout
from django.views.decorators.csrf import ensure_csrf_cookie

# Create your views here.

@ensure_csrf_cookie
def check_auth_stat(request: HttpRequest) -> HttpResponse:
    """Check the authentication status of requesting user. if authenticated, return user information"""
    if request.method == "GET":
        if request.user.is_authenticated:
            print("Authenticated")
            perm = Permission.objects.filter(user=request.user)
            logs = Log.objects.filter(user=request.user)
            return JsonResponse(
                {
                    'authenticated': True, 
                    'user': {
                        'initials': request.user.first_name.title()[:1] + request.user.last_name.title()[:1]\
                                    if request.user.first_name or request.user.last_name \
                                    else "-",
                        'name': f"{request.user.first_name.title()} {request.user.last_name.title()}".strip()\
                                if request.user.first_name or request.user.last_name \
                                else "-",
                        'perm': perm.first().get_perm_level_display() if perm.exists() else "Level 0 - Guest",
                        'logs': [l.as_dict() for l in logs.order_by('-date_time')]
                    }
                }
            )
        else:
            print("Not Authenticated")
            return JsonResponse(
                {
                    'authenticated': False, 
                    'user': None
                }
            )
    else:
        return JsonResponse({'error': "Not implemented method"}, status=501)


def log_in(request: HttpRequest) -> HttpResponse:
    """Log an existing user in"""
    if request.method == "POST":
        data = json.loads(request.body)
        u = authenticate(request=request, username=data['un'], password=data['pw'])
        if u:
            print("logged in as", u)
            login(request=request, user=u)
            return JsonResponse({'message': "Successful login"}, status=200)
        else:
            return JsonResponse({'error': "Incorrect username or password"}, status=401)
    else:
        return JsonResponse({'error': "Not implemented method"}, status=501)


def log_out(request: HttpRequest) -> HttpResponse:
    """Log the current user out"""
    print("Logging out of", request.user)
    logout(request=request)
    return JsonResponse({'message': "Logged out"})


def open_door(request: HttpRequest) -> HttpResponse:
    """Authenticate a door entry"""
    # needs authentication, POST
    if request.method == "POST":
        if request.user.is_authenticated:
            # TODO: implement
            pass
        else:
            JsonResponse({'error': "Must be logged in"}, status=401)
    else:
        return JsonResponse({'error': "Not implemented yet"}, status=501)

