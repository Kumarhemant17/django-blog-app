from django.shortcuts import render, get_object_or_404, redirect
from .models import Post
from .forms import PostForm
from django.contrib.auth.decorators import login_required

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