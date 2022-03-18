from django.shortcuts import render
from django.views.generic.edit import CreateView
from django.urls import reverse_lazy

from django.views import View
from students.accounts import UserAccount
from django.contrib.auth import authenticate, login, logout
from students.models import User
from students.register import Register
from django.shortcuts import render, redirect
from django.conf import settings
from .forms import UserRegistrationForm
from django.contrib import messages
from django.views.generic.edit import CreateView


def home(request):
    return render(request, "students/home.html")


class SignUp(CreateView):
    fields = ('username', 'first_name', 'middle_name',
              'last_name', 'email', 'date_of_birth', 'secondary_school', 'county', )
    success_url = reverse_lazy("login")
    model = User
    template_name = "registration/signup.html"
