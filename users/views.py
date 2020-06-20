from django.shortcuts import render, redirect
from django.contrib.auth import forms as auth_forms, logout as auth_logout, login as auth_login, authenticate
from django.views import generic as generic_views, View
from django.contrib.auth.decorators import user_passes_test
from django.utils.decorators import method_decorator
from django.contrib.auth.models import User
import json

class Registration(generic_views.FormView):
    template_name = 'register.html'
    form_class = auth_forms.UserCreationForm
    redirect_to = 'login'

    def post(self, request, *args, **kwargs):

        form = self.form_class(request.POST)

        if form.is_valid():
            user = form.save()
            auth_login(request, user)
            return redirect(self.redirect_to)

        return render(request, self.template_name, {'form': form})


class Login(generic_views.FormView):
    template_name = 'login.html'
    form_class = auth_forms.AuthenticationForm
    redirect_to = '/'

    def get(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return render(request, self.template_name, {'form': self.form_class})
        return redirect(self.redirect_to)


    def post(self, request, *args, **kwargs):

        form = self.form_class(data=request.POST)

        if form.is_valid():
            user = form.get_user()

            if user is not None:
                auth_login(request, user)
                return redirect(self.redirect_to)

        return render(request, self.template_name, {'form': form})



class Logout(View):
    redirect_to = 'login'

    def get(self, request, *args, **kwargs):
        auth_logout(request)
        return redirect(self.redirect_to)



