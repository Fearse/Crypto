from django.contrib import auth
from django.shortcuts import HttpResponseRedirect
from django.shortcuts import render

from .forms import UserAuthForm, UserRegForm


def login_check(request):
    if request.method == 'POST':
        form = UserAuthForm(data=request.POST)
        if form.is_valid():
            login = request.POST['username']
            password = request.POST['password']
            user = auth.authenticate(username=login, password=password)
            if user:
                auth.login(request, user)
                return HttpResponseRedirect('/acc')
    else:
        form = UserAuthForm()
    context = {'form': UserAuthForm()}
    return render(request, 'login/login_check.html', context)


def login_reg(request):
    if request.method == 'POST':
        form = UserRegForm(data=request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/login/check')
    else:
        form = UserRegForm()
    form = UserRegForm()
    context = {'form': form}
    return render(request, 'login/login_reg.html', context)
