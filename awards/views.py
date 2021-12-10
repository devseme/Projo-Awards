from django.shortcuts import render
from django.http  import HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .models import Profile

# Create your views here.

def index(request):
    
    return render(request, 'all-awards/index.html')

@login_required(login_url='/accounts/login/')
def profile(request):
    current_user = request.user
    profile = Profile.objects.filter(user_id=current_user.id).first()

    return render(request,"profile.html",{'profile':profile})
