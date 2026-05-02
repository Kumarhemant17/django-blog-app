from django.shortcuts import render, get_object_or_404, redirect
from .models import Post, Profile
from .forms import PostForm, CommentForm
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login

@login_required
def like_post(request, id):
    post = get_object_or_404(Post, id=id)

    if request.user in post.likes.all():
        post.likes.remove(request.user)   # unlike
    else:
        post.likes.add(request.user)      # like

    return redirect('detail', id=post.id)

def home(request):
    posts = Post.objects.all().order_by('-created_at')
    return render(request, 'home.html', {'posts': posts})

def post_detail(request, id):
    post = get_object_or_404(Post, id=id)
    return render(request, 'detail.html', {'post': post})

@login_required
def create_post(request):
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user   # VERY IMPORTANT
            post.save()
            return redirect('home')
    else:
        form = PostForm()

    return render(request, 'create.html', {'form': form})

@login_required
def edit_post(request, id):
    post = get_object_or_404(Post, id=id)

    # 🔒 Restrict access
    if request.user != post.author:
        return redirect('home')

    form = PostForm(request.POST or None, instance=post)

    if form.is_valid():
        form.save()
        return redirect('home')

    return render(request, 'create.html', {'form': form})

@login_required
def delete_post(request, id):
    post = get_object_or_404(Post, id=id)

    if request.user != post.author:
        return redirect('home')

    if request.method == 'POST':
        post.delete()
        return redirect('home')

    return render(request, 'confirm_delete.html', {'post': post})

def home(request):
    query = request.GET.get('q')

    if query:
        posts = Post.objects.filter(
            Q(title__icontains=query) | Q(content__icontains=query)
        ).order_by('-created_at')
    else:
        posts = Post.objects.all().order_by('-created_at')

    return render(request, 'home.html', {'posts': posts, 'query': query})

def post_detail(request, id):
    post = get_object_or_404(Post, id=id)
    comments = post.comments.all().order_by('-created_at')

    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid() and request.user.is_authenticated:
            comment = form.save(commit=False)
            comment.post = post
            comment.author = request.user
            comment.save()
            return redirect('detail', id=post.id)
    else:
        form = CommentForm()

    return render(request, 'detail.html', {
        'post': post,
        'comments': comments,
        'form': form
    })

@login_required
def like_post(request, id):
    post = get_object_or_404(Post, id=id)

    if request.user in post.likes.all():
        post.likes.remove(request.user)   # unlike
    else:
        post.likes.add(request.user)      # like

    return redirect('detail', id=post.id)

def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)   # auto login after signup
            return redirect('home')
    else:
        form = UserCreationForm()

    return render(request, 'signup.html', {'form': form})

def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()

            # save extra fields
            profile = user.profile
            profile.gender = request.POST.get('gender')
            profile.dob = request.POST.get('dob')
            profile.location = request.POST.get('location')
            profile.bio = request.POST.get('bio')

            if request.FILES.get('profile_pic'):
                profile.profile_pic = request.FILES.get('profile_pic')

            profile.save()

            login(request, user)
            return redirect('home')
    else:
        form = UserCreationForm()

    return render(request, 'signup.html', {'form': form})

@login_required
def profile(request):
    user_posts = Post.objects.filter(author=request.user).order_by('-created_at')

    return render(request, 'profile.html', {
        'posts': user_posts
    })

@login_required
def edit_profile(request):
    profile, created = Profile.objects.get_or_create(user=request.user)

    if request.method == 'POST':
        profile.gender = request.POST.get('gender')
        profile.dob = request.POST.get('dob')
        profile.location = request.POST.get('location')
        profile.bio = request.POST.get('bio')

        if request.FILES.get('profile_pic'):
            profile.profile_pic = request.FILES.get('profile_pic')

        profile.save()
        return redirect('profile')

    return render(request, 'edit_profile.html', {'profile': profile})