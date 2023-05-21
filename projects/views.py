from django.shortcuts import render, redirect
from .models import Project
from .forms import ProjectForm, ReviewForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .utils import searchProject, paginateProject
# Create your views here.
def home(request):
    return render(request, 'projects/home.html')

def project(request, pk):
    p = Project.objects.get(id=pk)
    form = ReviewForm()
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        review = form.save(commit=False)
        review.project = p
        review.owner = request.user.profile
        review.save()
        p.getVoteCount
        messages.success(request, 'Your review was successfully submitted!')
        return redirect('project', pk=p.id)
    return render(request, 'projects/project.html', {'project':p, 'form':form})

def projects(request):
    #ps = Project.objects.all()
    ps, search_query = searchProject(request)
    custom_range, ps = paginateProject(request, ps, 3)
    return render(request, 'projects/projects.html', {'projects':ps, 'search_query':search_query,'custom_range':custom_range})

@login_required(login_url="login")
def create_project(request):
    profile = request.user.profile
    form = ProjectForm()
    if request.method == "POST":
        form = ProjectForm(request.POST, request.FILES)
        if form.is_valid():
            project = form.save(commit = False)
            project.owner = profile
            project.save()
            form.save()
            messages.success(request, 'Project was created successfully')
            return redirect('account')

    return render(request, 'projects/project-form.html', {'form' :form})

@login_required(login_url="login")
def editProject(request, pk):
    profile = request.user.profile
    project = profile.project_set.get(id=pk)
    form = ProjectForm(instance=project)
    if request.method == "POST":
        form = ProjectForm(request.POST, request.FILES, instance = project)
        if form.is_valid():
            form.save()
            messages.success(request, 'Project was updated successfully')
            return redirect('account')
    return render(request, 'projects/project-form.html', {'form':form})

@login_required(login_url="login")
def removeProject(request, pk):
    profile = request.user.profile
    project = profile.project_set.get(id=pk)
    if request.method == "POST":
        project.delete()
        messages.success(request, 'Project was deleted successfully')
        return redirect("account")
    return render(request, 'projects/delete-project.html', {'project':project})


