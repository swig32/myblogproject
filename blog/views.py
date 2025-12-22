from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from .models import Post, Comment
from .forms import PostForm  # <--- FIX 1: Added this missing import
from members.models import Member

def post_list(request):
    # FIX 2: Changed 'created_at' to 'date_posted'
    posts = Post.objects.all().order_by('-date_posted')

    latest_members = Member.objects.all().order_by('-joined_date')[:5]

    context = {
        'posts': posts,
        'latest_members': latest_members,
    }
    return render(request, 'blog/post_list.html', context)


def like_post(request, pk):
    post = get_object_or_404(Post, id=request.POST.get('post_id'))
    if post.likes.filter(id=request.user.id).exists():
        post.likes.remove(request.user)  # Unlike
    else:
        post.likes.add(request.user)  # Like

    return redirect('post_detail', pk=pk)


def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    # FIX 3: Changed 'created_at' to 'date_posted' (or whatever your comment date field is)
    # If your Comment model still uses 'created_at', leave it.
    # But for Post, we must use 'date_posted'.
    comments = post.comments.all().order_by('-created_at')
    return render(request, 'blog/post_detail.html', {'post': post, 'comments': comments})

def register(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')

        error = None
        if not username or not password1:
            error = 'Username and password are required.'
        elif password1 != password2:
            error = 'Passwords do not match.'
        elif User.objects.filter(username=username).exists():
            error = 'Username already taken.'

        if error:
            return render(request, 'blog/register.html', {'error': error})

        user = User.objects.create_user(username=username, password=password1)
        login(request, user)
        return redirect('post_list')

    return render(request, 'blog/register.html')


def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('post_list')
        else:
            return render(request, 'blog/login.html',
                          {'error': ' Invalid Username or Password entered'})
    return render(request, 'blog/login.html')


def logout_view(request):
    logout(request)
    return redirect('post_list')


@login_required
def post_create(request):
    if request.method == 'POST':
        # Added request.FILES to capture the photo/video
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect('post_list')
    else:
        form = PostForm()
    return render(request, 'blog/post_form.html', {'form': form})

@login_required
def add_comment(request, pk):
    post = get_object_or_404(Post, pk=pk)

    if request.method == 'POST':
        text = request.POST.get('text')
        # Capture the uploaded file
        media = request.FILES.get('media')

        if not text:
            comments = post.comments.all().order_by('-created_at')
            return render(
                request, 'blog/post_detail.html',
                {'post': post, 'comments': comments, 'error': "comment text is required!"}
            )

        # Save the comment with the media file
        Comment.objects.create(post=post, author=request.user, text=text, media=media)
        return redirect('post_detail', pk=post.pk)
    return redirect('post_detail', pk=post.pk)


@login_required
def post_edit(request, pk):
    post = get_object_or_404(Post, pk=pk)

    # Security: Ensure only the author can edit
    if post.author != request.user:
        return HttpResponseForbidden('You are not allowed to edit this post!')

    if request.method == 'POST':
        # 'instance=post' updates the specific post instead of creating a new one
        form = PostForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            form.save()
            return redirect('post_detail', pk=post.pk)
    else:
        # Pre-fills the form with the current post data
        form = PostForm(instance=post)

    return render(request, 'blog/post_form.html', {
        'form': form,
        'post': post,
        'edit_mode': True  # We'll use this to change the title in the HTML
    })
@login_required
def post_delete(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if post.author != request.user:
        return HttpResponseForbidden('You are not allowed to delete this post!')
    if request.method == 'POST':
        post.delete()
        return redirect('post_list')
    return render(request, 'blog/post_confirm_delete.html', {'post': post})


@login_required
def comment_delete(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    # Security: Check if the logged-in user is the one who wrote the comment
    if comment.author != request.user:
        return HttpResponseForbidden("You cannot delete someone else's comment!")

    post_pk = comment.post.pk
    comment.delete()
    return redirect('post_detail', pk=post_pk)