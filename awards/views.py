from django.shortcuts import render,redirect, get_object_or_404
from django.http  import HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .models import Profile,Project,Rating
from .forms import ShowProjectForm,EditProfileForm,ProfileForm
from django.http  import HttpResponse,HttpResponseRedirect
from rest_framework.views import APIView
from .permissions import IsAdminOrReadOnly
from awards import serializer
from django.http import HttpResponseRedirect, Http404
from .serializer import ProfileSerializer,ProjectSerializer
from rest_framework.response import Response




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
                return redirect('profile') 
            
    ctx = {"form":form}
    return render(request, 'update_profile.html', ctx) 
       
@login_required(login_url='/accounts/login/')
def create_profile(request):
    current_user = request.user
    title = "Create Profile"
    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES)
        if form.is_valid():
            profile = form.save(commit=False)
            profile.user = current_user
            profile.save()
        return HttpResponseRedirect('/')

    else:
        form = ProfileForm()
    return render(request, 'create_profile.html', {"form": form, "title": title})


@login_required(login_url='/accounts/login/')
def search_project(request):
    if 'search' in request.GET and request.GET['search']:
        search_term = request.GET.get('search').lower()
        images = Project.search_project_name(search_term)
        message = f'{search_term}'

        return render(request, 'result.html', {'found': message, 'images': images})
    else:
        message = 'Not found'
        return render(request, 'result.html', {'danger': message})
def project_details(request, project_id):
    project = Project.objects.get(id=project_id)
    rating = Rating.objects.filter(project = project)
    return render(request, "project_details.html", {"project": project,"rating":rating})

@login_required(login_url='/accounts/login/')
def rate_project(request,id):
    if request.method == 'POST':
        project = Project.objects.get(id=id)
        current_user = request.user

        design_rate = request.POST['design']
        content_rate = request.POST['content']
        usability_rate = request.POST['usability']

        Rating.objects.create(
            project=project,
            user=current_user,
            design_rate=design_rate,
            usability_rate=usability_rate,
            content_rate=content_rate,
            avg_rate=round((float(design_rate)+float(usability_rate)+float(content_rate))/3,2),
        )
        return render(request,'project_details.html',{"project":project})

    else:
        project = Project.objects.get(id=id)
 
        return render(request,'project_details.html',{"project":project})
class ProjectList(APIView):
    permission_classes = (IsAdminOrReadOnly,)
    def get(self,request,format=None):
        projects = Project.objects.all()
        serializer = ProfileSerializer(projects,many=True)
        return Response(serializer.data)

class ProfileList(APIView):
    permission_classes = (IsAdminOrReadOnly,)
    def get(self,request,format=None):
        profiles = Profile.objects.all()
        serializer = ProjectSerializer(profiles,many=True)
        return Response(serializer.data)

class ProjectList(APIView):
    permission_classes = (IsAdminOrReadOnly,)
    def get(self,request,format=None):
        projects = Project.objects.all()
        serializer = ProfileSerializer(projects,many=True)
        return Response(serializer.data)        

   


