from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout

def login_view(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect('home')
        else:
            return render(request, 'accounts/login.html', {'error': '아이디 또는 비밀번호가 틀렸습니다.'})
    return render(request, 'accounts/login.html')

def logout_view(request):
    logout(request)
    return redirect('home')

def signup_view(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        password2 = request.POST['password2']

        if password != password2:
            return render(request, 'accounts/signup.html', {'error': '비밀번호가 일치하지 않습니다.'})

        if User.objects.filter(username=username).exists():
            return render(request, 'accounts/signup.html', {'error': '이미 존재하는 아이디입니다.'})

        user = User.objects.create_user(username=username, password=password)
        login(request, user)  # 회원가입 후 자동 로그인
        return redirect('home')

    return render(request, 'accounts/signup.html')