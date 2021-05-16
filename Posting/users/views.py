from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import UserRegisterForm, UserUpdateForm, ProfileUpdateForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .models import Profile
from django.db.models import ObjectDoesNotExist


# Create your views here.
def register_view(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            user_name = form.cleaned_data.get('username')
            messages.success(request, f'Your account has been created. You able to login now !!!')
            return redirect('login')
        else:
            return render(request, 'users/register.html', {'form': form})

    else:
        form = UserRegisterForm()

        return render(request, "users/register.html", {'form': form})


@login_required
def profile_view(request):
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        try:
            p_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)
        except ObjectDoesNotExist:
            Profile.objects.create(profile_img=request.FILES.get('profile_img'), user=request.user)
            p_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, f'Successfully Updated!!!')
            return redirect('profile')
        return redirect('profile')
    else:
        u_form = UserUpdateForm(instance=request.user)
        try:
            p_form = ProfileUpdateForm(instance=request.user.profile)
        except ObjectDoesNotExist:
            p_form = ProfileUpdateForm()
    context = {
        'u_form': u_form,
        'p_form': p_form,
    }
    return render(request, "users/profile.html", context)
