from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Member
from .forms import RegisterForm
from django.db import models

def main(request):
    return render(request, 'main.html')

def members(request):
    query = request.GET.get('q')
    if query:
        # Filters by last name or first name (case-insensitive)
        mymembers = Member.objects.filter(
            models.Q(lastname__icontains=query) |
            models.Q(firstname__icontains=query)
        )
    else:
        mymembers = Member.objects.all()

    return render(request, 'all_member.html', {'mymembers': mymembers})

def details(request, id):
    mymember = get_object_or_404(Member, id=id)
    return render(request, 'details.html', {'mymember': mymember})

def register_user(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = RegisterForm()
    return render(request, 'blog/register.html', {'form': form})


@login_required
def update_profile(request):
    member = request.user.member  # Assumes User has a related Member profile
    if request.method == 'POST':
        # Get the files from the request
        if request.FILES.get('profile_pic'):
            member.profile_pic = request.FILES.get('profile_pic')
            member.save()
            return redirect('post_list')

    return render(request, 'members/update_profile.html', {'member': member})