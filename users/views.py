from django.shortcuts import render, redirect
from .models import Profile, Message
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .fomrs import CustomUserCreationForm, profileForm, skillForm, messageForm
from django.contrib.auth.decorators import login_required
from .utils import searchProfiles, paginateProfiles
# Create your views here.
def profiles(request):
    profs, search_query = searchProfiles(request)
    custom_range, profs = paginateProfiles(request, profs, 2)
    return render(request, 'users/profiles.html', {'profiles':profs, 'search_query':search_query, 'custom_range':custom_range})


def userProfile(request, pk):
    profile = Profile.objects.get(id=pk)
    topSkills = profile.skil_set.exclude(description__exact = "")
    otherSkills = profile.skil_set.filter(description = "")
    return render(request, 'users/user-profile.html', {'profile':profile, "topSkills" : topSkills, 'otherSkills':otherSkills})

def loginUser(request):
    page = "login"
    if request.user.is_authenticated:
        return redirect('profiles')
    if request.method == "POST":
        username = request.POST['username'].lower()
        password = request.POST['password']
        try:
            user = User.objects.get(username=username)
        except:
            messages.error(request, "user does not exist!")
        user = authenticate(request, username = username, password = password)
        if user is not None:
            login(request, user)
            return redirect(request.GET['next'] if 'next' in request.GET else 'account')
        else:
            messages.error(request,"username or password in incorrect")
    return render(request, 'users/login-register.html')

def logoutUser(request):
    logout(request)
    messages.info(request, "User was logged out!")
    return redirect('login')

def registerUser(request):
    page = "register"
    form = CustomUserCreationForm()
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()
            messages.success(request, 'user account was created!')
            login(request, user)
            return redirect('edit-account')
        else:
            messages.error(request, 'An error occurred during registration')
    contex = {'page':page, "form":form}
    return render(request, 'users/login-register.html', contex)

@login_required(login_url='login')
def userAccount(request):
    profile = request.user.profile
    skills = profile.skil_set.all()
    projects = profile.project_set.all()
    context = {'profile':profile, 'skills':skills, 'projects':projects}
    return render(request, 'users/account.html', context)


@login_required(login_url='login')
def editAccount(request):
    profile = request.user.profile
    form = profileForm(instance=profile)
    if request.method == "POST":
        form = profileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('account')
    contex = {'form':form}
    return render(request, 'users/profile-form.html', contex)

@login_required(login_url='login')
def createSkill(request):
    profile = request.user.profile
    form = skillForm()
    if request.method == "POST":
        form = skillForm(request.POST)
        if form.is_valid():
            skill = form.save(commit=False)
            skill.owner = profile
            skill.save()
            messages.success(request, 'Skill was added successfully')
            return redirect('account')
    contex = {'form':form}
    return render(request, 'users/skill-form.html', contex)

@login_required(login_url='login')
def updateSkill(request, pk):
    profile = request.user.profile
    skill = profile.skil_set.get(id=pk)
    form = skillForm(instance=skill)
    if request.method == "POST":
        form = skillForm(request.POST, instance=skill)
        if form.is_valid():
            form.save()
            messages.success(request, 'Skill was updated successfully')
            return redirect('account')
    contex = {'form':form}
    return render(request, 'users/skill-form.html', contex)

@login_required(login_url='login')
def deleteSkill(request, pk):
    profile = request.user.profile
    skill = profile.skil_set.get(id=pk)
    if request.method == "POST":
        skill.delete()
        messages.success(request, 'Skill was deleted successfully')
        return redirect('account')
    contex = {'skill':skill}
    return render(request, 'users/skill-delete.html', contex)


@login_required(login_url='login')
def inbox(request):
    profile = request.user.profile
    masseageRequests = profile.messages.all()
    unreadCount = masseageRequests.filter(is_read = False).count()
    context = {"messageRequests":masseageRequests, 'unreadCount':unreadCount}
    return render(request, 'users/inbox.html', context)

@login_required(login_url='login')
def veiwMessage(request, pk):
    profile = request.user.profile
    message = profile.messages.get(id=pk)
    if message.is_read == False:
        message.is_read = True
        message.save()
    context = {'message':message}
    return render(request, 'users/message.html', context)

def createMessaage(request, pk):
    recipient = Profile.objects.get(id=pk)
    form = messageForm()
    try:
        sender = request.user.profile
    except:
        sender = None
    if request.method == "POST":
        form = messageForm(request.POST)
        if form.is_valid():
            message = form.save(commit=False)
            message.sender = sender
            message.recipient = recipient

            if sender:
                message.name = sender.name
                message.email = sender.email
            message.save()
            messages.success(request, 'Your message was successfully sent!')
            return redirect('user-profile', pk=recipient.id)
    contex = {'recipient':recipient, 'form':form}
    return render(request, 'users/message-form.html', contex)