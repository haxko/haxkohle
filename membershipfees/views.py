from django.shortcuts import render, redirect
from django.http import HttpResponse

user_logged_in = False

def has_persmission(user, permission):
    return True

def home(request):
    if not user_logged_in:
        return redirect('index')
    if not has_persmission(request.user, 'access_member_data'):
        return redirect('membershipfees_me')
    return HttpResponse('membershipfees_members')

def user_status(request):
    return render(request, 'membershipfees/me.html', {})
    #return HttpResponse('User Status')

def members_status(request):
    return HttpResponse('Members Status')
