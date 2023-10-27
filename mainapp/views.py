from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login, authenticate, logout
from mainapp.models import Profile, tag, post, comment, followship
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
    if request.method == 'POST' and request.user.is_authenticated:
        form = forms.commentForm(request.POST)
        
        if form.is_valid():
            comment_object = form.save(commit=False)
            comment_object.user = request.user
            comment_object.post = post_object
            comment_object.save()
            messages.success(request, 'comment created successfully')
            return redirect('post', pk=post_object.id)
    elif request.method == 'POST' and not request.user.is_authenticated:
        return redirect('login')   
    
    related_comments = comment.objects.filter(post=post_object)
    
    context = {'post':post_object, 'comments': related_comments, 'form': form}
    return render(request, 'post.html', context)

@login_required(login_url='login')
def profile_page(request, username):
    related_user = get_object_or_404(User, username=username)
    profile_object = get_object_or_404(Profile, related_user=related_user)
    related_posts = related_user.post_set.all()
    is_following = followship.objects.filter(related_user=request.user, followed_user=related_user).count()
    if is_following == 0:
        print(is_following)
        is_following = False
    else:
        is_following = True
    context = {
        'user': related_user, 
        'profile': profile_object, 
        'media': settings.MEDIA_URL, 
        'posts': related_posts, 
        'is_following': is_following,
        'followers': followship.followers_count(user=related_user),
        'following': followship.following_count(followed_by=related_user),
    }
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

@login_required(login_url='login')
def follow(request, username):
    related_user = request.user
    followed_user = get_object_or_404(User, username=username)
    
    is_following = followship.objects.filter(related_user=related_user, followed_user=followed_user)
    
    if is_following.count() == 0 :
        print("add")
        followship.objects.create(related_user=related_user, followed_user=followed_user)
        return redirect('profile', username=followed_user)
    else:
        print("remove")
        is_following.delete()
        return redirect('profile', username=followed_user)
    
def logout_page(request):
    logout(request)
    return redirect('login')

@login_required(login_url='login')
def add_rate(request, username):
    related_user = get_object_or_404(User, username=username)
    if request.method == 'POST':
        rate = request.POST.get('rate')
        related_profile = Profile.objects.filter(related_user=related_user).first()
        res = (related_profile.rate * related_profile.rate_count)
        res += int(rate)
        res /= (related_profile.rate_count+1)
        related_profile.rate_count += 1
        related_profile.rate = res
        related_profile.save()
        messages.success(request, 'Rate added successfully')
        return redirect('profile', related_user.username)
    
    
@login_required(login_url='login')
def edit_profile(request, username):
    related_user = get_object_or_404(User, username=username)
    related_profile = Profile.objects.filter(related_user=related_user).first()
    form = forms.profileForm(instance=related_profile)
    
    if request.method == 'POST':
        form = forms.profileForm(request.POST, request.FILES, instance=related_profile)
        print(form.data)
        if form.is_valid():
            # profile_form = form.save(commit=False)
            # profile_form.related_user = related_user
            form.save()
            messages.success(request, 'profile updated successfully')
            return redirect('profile', related_user.username)
        else:
            form = forms.profileForm(instance=related_profile)
            messages.error(request, 'entries are invalid')
    
    return render(request, 'profile_edit.html', {'form': form}) 
    
def search(request):
    pass