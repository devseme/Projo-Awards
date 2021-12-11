from django.shortcuts import render,redirect, get_object_or_404
from django.http  import HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .models import Profile,Project
from .forms import ShowProjectForm,EditProfileForm
# Create your views here.

def index(request):
    ip =Project.objects.all().order_by('-id')

    return render(request, 'all-awards/index.html',{'ip':ip})

@login_required(login_url='/accounts/login/')
def profile(request):
    current_user = request.user
    profile = Profile.objects.filter(user_id=current_user.id).first()
    project = Project.objects.filter(user_id=current_user.id)
      

    return render(request,"profile.html",{'profile':profile ,'project':project})

@login_required(login_url='/accounts/login/')
def upload(request):
    if request.method == 'POST':
        form=ShowProjectForm(request.POST,request.FILES)
        if form.is_valid():
            ip =form.save(commit=False)
            ip.save()
            return redirect('/')
    else:
        form=ShowProjectForm()
    return render(request,"show_projo.html",{'form':form})  

@login_required(login_url='/accounts/login/')
def update_profile(request,id):
    user = User.objects.get(id=id)
    profile = Profile.objects.get(user = user)
    form = EditProfileForm(instance=profile)
    if request.method == "POST":
            form = EditProfileForm(request.POST,request.FILES,instance=profile)
            if form.is_valid():  
                
                profile = form.save(commit=False)
                profile.save()
                return redirect('profile' ,username=user.username) 
            
    ctx = {"form":form}
    return render(request, 'update_profile.html', ctx)    



