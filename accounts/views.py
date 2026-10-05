from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from .forms import UserRegisterForm, UserUpdateForm, ProfileUpdateForm
from items.models import Item
from claims.models import ClaimRequest

def register_view(request):
    if request.user.is_authenticated:
        return redirect('accounts:dashboard')
    
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, f"Welcome to BAIUST Lost & Found, {user.first_name or user.username}! Your account has been registered.")
            return redirect('accounts:dashboard')
    else:
        form = UserRegisterForm()
    
    return render(request, 'accounts/register.html', {'form': form})

def login_view(request):
    if request.user.is_authenticated:
        return redirect('accounts:dashboard')
    
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, f"Welcome back, {user.username}!")
                next_url = request.GET.get('next')
                if next_url:
                    return redirect(next_url)
                return redirect('accounts:dashboard')
        else:
            messages.error(request, "Invalid username or password. Please try again.")
    else:
        form = AuthenticationForm()
        
    return render(request, 'accounts/login.html', {'form': form})

def logout_view(request):
    logout(request)
    messages.info(request, "You have been logged out.")
    return redirect('items:home')

@login_required
def profile_view(request):
    # Ensure profile exists for older users or superusers
    if not hasattr(request.user, 'profile'):
        from .models import UserProfile
        UserProfile.objects.create(user=request.user, student_id=f"TEMP-{request.user.id}")

    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, "Your profile details have been updated.")
            return redirect('accounts:profile')
    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)
        
    return render(request, 'accounts/profile.html', {
        'u_form': u_form,
        'p_form': p_form
    })

@login_required
def dashboard_view(request):
    # Items reported by current user
    lost_items = Item.objects.filter(reported_by=request.user, item_type='LOST').order_by('-created_at')
    found_items = Item.objects.filter(reported_by=request.user, item_type='FOUND').order_by('-created_at')
    
    # Claims submitted by current user
    my_claims = ClaimRequest.objects.filter(claimant=request.user).order_by('-created_at')
    
    # Claims received on items reported by current user
    incoming_claims = ClaimRequest.objects.filter(item__reported_by=request.user).order_by('-created_at')

    context = {
        'lost_items': lost_items,
        'found_items': found_items,
        'my_claims': my_claims,
        'incoming_claims': incoming_claims,
    }
    return render(request, 'accounts/dashboard.html', context)
