from django.shortcuts import render
from django.http import JsonResponse

# Create your views here.

def login(request):
    """Log an existing user in"""
    return JsonResponse({'error': "Not implemented yet"}, status=501)


def logout(request):
    """Log the current user out"""
    return JsonResponse({'error': "Not implemented yet"}, status=501)


def auth(request):
    """Authenticate a door entry"""
    return JsonResponse({'error': "Not implemented yet"}, status=501)


def logs(request):
    """Return the entry logs of current user"""
    return JsonResponse({'error': "Not implemented yet"}, status=501)


def profile(request):
    """Return the profile data (name and perm. level) of the current user"""
    return JsonResponse({'error': "Not implemented yet"}, status=501)