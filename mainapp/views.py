from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login, authenticate, logout
from mainapp.models import Profile, tag, post, comment
from django.db.models import Q
from django.conf import settings
from django.contrib.auth.decorators import login_required, permission_required
from mainapp import forms

def home(request):
    q = request.GET.get('q') if request.GET.get('q') != None else ''
    latest_posts = post.objects.filter(
        Q(title__icontains=q)|
        Q(user__username__icontains=q)
    )
    all_tags = tag.objects.all()
    context = {'posts': latest_posts, 'tags':all_tags}
    return render(request, 'home.html', context)

def login_page(request):
    if request.method == 'POST':
        username = request.POST.get('username').lower()
        password = request.POST.get('password')
        try:
            user = User.objects.get(username=username)
        except:
            messages.error(request, 'User does not exist')
            return redirect('login')
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'Invalid login or password.')   
            return redirect('login')
        
    return render(request, 'login.html')

def register_page(request):
    form = UserCreationForm()
    
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            form.save()
            user_profile = Profile(related_user=user)
            user_profile.save()
            login(request, user)
            return redirect('home')
        else:
            print(form)
            messages.error(request, 'An error happend during registertion :(')
    context = {'form': form}
    return render(request, 'register.html', context)

def post_page(request, pk):
    form = forms.commentForm()
    
    post_object = get_object_or_404(post, id=pk)
    if request.method == 'POST':
        form = forms.commentForm(request.POST)
        
        if form.is_valid():
            comment_object = form.save(commit=False)
            comment_object.user = request.user
            comment_object.post = post_object
            comment_object.save()
            messages.success(request, 'comment created successfully')
            return redirect('post', pk=post_object.id)
        
    related_comments = comment.objects.filter(post=post_object)
    
    context = {'post':post_object, 'comments': related_comments, 'form': form}
    return render(request, 'post.html', context)

def profile_page(request, username):
    related_user = get_object_or_404(User, username=username)
    profile_object = get_object_or_404(Profile, related_user=related_user)
    related_posts = related_user.post_set.all()
    context = {'user': related_user, 'profile': profile_object, 'media': settings.MEDIA_URL, 'posts': related_posts}
    return render(request, 'profile.html', context)

@login_required(login_url='login')
def create_post(request):
    form = forms.postForm()
    
    if request.method == 'POST':
        form = forms.postForm(request.POST)
        if form.is_valid():
            post_object = form.save(commit=False)
            post_object.user = request.user
            post_object.save()
            messages.success(request, 'Post created successfully')
            return redirect('post', pk=post_object.id)
            
    return render(request, 'edit_post.html', {'form': form})

@login_required(login_url='login')
def editPost(request, pk):
    post_object = get_object_or_404(post,id=pk)
    form = forms.postForm(instance=post_object)
    if request.method == 'POST':
        form = forms.postForm(request.POST, instance=post_object)
        if form.is_valid():
            form.save()
            messages.success(request, 'post updated successfully')
        else:
            messages.error(request, 'entries are invalid')
    
    return render(request, 'edit_post.html', {'form': form}) 