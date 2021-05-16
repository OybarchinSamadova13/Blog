from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib import messages
from .models import Post, Comment
from .forms import PostUpdateForm, PostCreateForm, CommentCreateForm
from django.db.models import ObjectDoesNotExist, Q
from django.contrib.auth.decorators import login_required


# Create your views here.

def home_view(request):
    q = request.GET.get('q')
    if q is None:
        posts = Post.objects.all().order_by('-date_posted')
    else:
        posts = Post.objects.filter(Q(title__icontains=q) | Q(author__username__icontains=q)).order_by('-date_posted')
    context = {
        'posts': posts,
        'q': q,
    }
    return render(request, "blog/home.html", context)


def post_details(request, pk):
    if request.method == 'POST':
        post = Post.objects.get(pk=pk)
        form = CommentCreateForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            Comment.objects.create(author=request.user,
                                   content=data['comment'],
                                   post=post)
        form = CommentCreateForm()
        comments = Comment.objects.all()
        return render(request, 'blog/post_detail.html', {'post': post, 'comments': comments, 'form': form})

    else:
        form = CommentCreateForm()
        comments = Comment.objects.all()
        try:
            post = Post.objects.get(pk=pk)
            return render(request, 'blog/post_detail.html', {'post': post, 'comments': comments, 'form': form})
        except ObjectDoesNotExist:
            return HttpResponse('There is not a post with this id')


@login_required
def post_update(request, pk):
    try:
        post = Post.objects.get(pk=pk)
        if request.method == "GET":
            if request.user.username == post.author.username:
                form = PostUpdateForm(instance=post)
            else:
                return HttpResponse('You can not change the post of others')
            context = {
                'form': form,
            }
            return render(request, 'blog/post_update.html', context)
        else:
            form = PostUpdateForm(request.POST, request.FILES, instance=post)
            if form.is_valid():
                form.save()
                messages.success(request, 'Successfully Updated !!!')
                return redirect(f'home_view')
    except ObjectDoesNotExist:
        return HttpResponse('There is not a post with this id')


@login_required
def post_delete(request, pk):
    try:
        if request.method == "GET":
            return render(request, 'blog/post_delete.html')
        else:
            Post.objects.get(pk=pk).delete()
            messages.success(request, 'Successfully Deleted !!!')
            return redirect(f'home_view')
    except ObjectDoesNotExist:
        return HttpResponse('There is not a post with this id')


@login_required
def post_create(request):
    if request.method == "GET":
        form = PostUpdateForm()
        return render(request, 'blog/post_create.html', {'form': form})
    else:
        form = PostCreateForm(request.POST, request.FILES)
        if form.is_valid():
            data = form.cleaned_data
            Post.objects.create(title=data['title'],
                                img=data['img'],
                                content=data['content'],
                                author=request.user, )
            messages.success(request, 'Post Successfully created !!!')
        return redirect('home_view')


def post_author(request, pk):
    try:
        post = Post.objects.get(pk=pk)
        return render(request, 'blog/post_author.html', {'post': post, })
    except ObjectDoesNotExist:
        return HttpResponse('There is not a post author with this id')


def about(request):
    return render(request, 'blog/about.html')
