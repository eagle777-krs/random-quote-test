from django.contrib.auth.hashers import check_password
from django.shortcuts import render, redirect
from .models import User
from .forms import UserLoginForm, UserRegistrationForm

def register_view(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = UserRegistrationForm()
    return render(request, 'register.html', {'form': form})


def login_view(request):
    form = UserLoginForm(request.POST or None)
    if form.is_valid():
        username = form.cleaned_data['username']
        password = form.cleaned_data['password']
        try:
            user = User.objects.get(username=username)
            if check_password(password, user.password):
                request.session['user_id'] = user.id
                return redirect('quotes:index')
            else:
                form.add_error('password', 'Неверный пароль')
        except User.DoesNotExist:
            form.add_error('username', 'Пользователь не найден')
    return render(request, 'login.html', {'form': form})
