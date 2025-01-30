import json, datetime as Dt
from django.contrib.auth.models import User
from .models import Door, Permission, Log
from django.http import HttpRequest, HttpResponse, JsonResponse
from django.contrib.auth import authenticate, login, logout
from django.views.decorators.csrf import ensure_csrf_cookie
from django.utils.timezone import make_aware

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
                        'perm': perm.first().get_perm_level_display(),
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
    if request.method == "POST":
        if request.user.is_authenticated:
            data = json.loads(request.body)
            received_door = None
            try:
                received_door = Door.objects.get(id=data['id'])
            except Door.DoesNotExist:
                print("Door does not exist")
                return JsonResponse({'error': "Door could not be identified"}, status=400)
            
            if (received_door.perm_level <= Permission.objects.filter(user=request.user).first().perm_level):
                # User has permission to access the door, make log entry and return
                Log.objects.create(
                    user=request.user,
                    door=received_door,
                    date_time=make_aware(Dt.datetime.now())
                )
                print(request.user, "opened:", received_door)
                return JsonResponse({'message': "Permission granted, Door unlocked"}, status=200)
            else:
                # User doesn't have permission to access the door, make log entry and return error
                Log.objects.create(
                    user=request.user,
                    door=received_door,
                    date_time=make_aware(Dt.datetime.now()),
                    perm_granted=False
                )
                print(request.user, "tried to open:", received_door)
                return JsonResponse({'error': "User does not have necessary permission."}, status=403)
        else:
            return JsonResponse({'error': "User must be logged in"}, status=401)
    else:
        return JsonResponse({'error': "Not implemented yet"}, status=501)

