from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, PasswordChangeForm
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout
from django.contrib.auth import get_user_model, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from .forms import UserCustomChangeForm

# Create your views here.
def signup(request):
    if request.user.is_authenticated:
        return redirect('posts:list')
        
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            auth_login(request, user)
            return redirect('posts:list')
        
    else:
        form = UserCreationForm()
    context = {
        'form': form
    }
    return render(request, 'accounts/signup.html', context)
    
    
def login(request):
    if request.user.is_authenticated:
        return redirect('posts:list')
        
    if request.method == 'POST':
        form = AuthenticationForm(request, request.POST)
        if form.is_valid():
            auth_login(request, form.get_user())
            # return redirect(request.POST.get('next') or 'posts:list')
            return redirect(request.GET.get('next') or 'posts:list')
    else:
        form = AuthenticationForm()
    context = {
        'form': form,
        # 'next': request.GET.get('next', ''),
    }
    return render(request, 'accounts/login.html', context)
    
    
def logout(request):
    auth_logout(request)
    return redirect('posts:list')

    
def people(request, username):
    people = get_object_or_404(get_user_model(), username=username)
    context = {
        'people': people,
    }
    return render(request, 'accounts/people.html', context)


@login_required
def update(request):
    if request.method == 'POST':
        user_change_form = UserCustomChangeForm(request.POST, instance=request.user)
        if user_change_form.is_valid():
            user_change_form.save()
            # return redirect('posts:list')
            return redirect('people', request.user.username)
    else:
        user_change_form = UserCustomChangeForm(instance=request.user)
    context = {
        'user_change_form': user_change_form,
    }
    return render(request, 'accounts/update.html', context)
    

@login_required    
def delete(request):
    if request.method == 'POST':
        request.user.delete()
    return redirect('posts:list')
    

@login_required
def password(request):
    if request.method == 'POST':
        password_change_form = PasswordChangeForm(request.user, request.POST)
        if password_change_form.is_valid():
            user = password_change_form.save()
            update_session_auth_hash(request, user)
            return redirect('people', request.user.username)
    else:
        password_change_form = PasswordChangeForm(request.user)
    context = {
        'password_change_form': password_change_form,
    }
    return render(request, 'accounts/password.html', context)
    