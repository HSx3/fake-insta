from django.shortcuts import render, redirect, get_list_or_404, get_object_or_404
from .models import Post, Image
from .forms import PostForm, ImageForm
from django.contrib.auth.decorators import login_required

# Create your views here.
def list(request):
    posts = get_list_or_404(Post.objects.order_by('-pk'))
    context = {
        'posts': posts,
    }
    return render(request, 'posts/list.html', context)

@login_required    
def create(request):
    # 새 글 등록, 수정 동작
    if request.method == 'POST':
        # post_form = PostForm(request.POST, request.FILES)
        post_form = PostForm(request.POST)
        if post_form.is_valid():
            # post_form.save()
            post = post_form.save(commit=False)
            post.user = request.user
            post.save()
            for image in request.FILES.getlist('file'):
                request.FILES['file'] = image
                image_form = ImageForm(files=request.FILES)
                if image_form.is_valid():
                    image = image_form.save(commit=False)
                    image.post = post
                    image.save()
            return redirect('posts:list')
    
    # 새 글 작성페이지
    else:
        post_form = PostForm()
        image_form = ImageForm()
    context = {
        'post_form': post_form,
        'image_form': image_form,
    }
    return render(request, 'posts/form.html', context)

# def detail(request, post_pk):
#     post = get_object_or_404(Post, pk=post_pk)
#     context = {
#         'post': post,
#     }
#     return render(request, 'posts/detail.html', context)

@login_required
def update(request, post_pk):
    post = get_object_or_404(Post, pk=post_pk)  # 수정할 글을 가져오기 위해
    
    if post.user != request.user:
        return redirect('posts:list')
    
    if request.method == 'POST':
        post_form = PostForm(request.POST, instance=post)
        if post_form.is_valid():
            post_form.save()
            return redirect('posts:list')
            # return redirect('posts:detail', post.pk)
    else:
        post_form = PostForm(instance=post)     # 수정할 데이터를 가져와야함
    context = {
        'post_form': post_form,
        'post': post,
    }
    return render(request, 'posts/form.html', context)
    
def delete(request, post_pk):
    post = get_object_or_404(Post, pk=post_pk)
    
    if post.user != request.user:
        return redirect('posts:list')
    
    if request.method == 'POST':
        post.delete()
    return redirect('posts:list')
    # else:
    #     return redirect('posts:detail', post.pk)