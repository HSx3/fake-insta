from django.shortcuts import render, redirect, get_list_or_404, get_object_or_404
from .models import Post
from .forms import PostForm

# Create your views here.
def list(request):
    posts = get_list_or_404(Post.objects.order_by('-pk'))
    context = {
        'posts': posts,
    }
    return render(request, 'posts/list.html', context)
    
def create(request):
    # 새 글 등록, 수정 동작
    if request.method == 'POST':
        post_form = PostForm(request.POST, request.FILES)
        if post_form.is_valid():
            post_form.save()
            return redirect('posts:list')
    
    # 새 글 작성페이지
    else:
        post_form = PostForm()
    context = {
        'post_form': post_form,
    }
    return render(request, 'posts/form.html', context)

# def detail(request, post_pk):
#     post = get_object_or_404(Post, pk=post_pk)
#     context = {
#         'post': post,
#     }
#     return render(request, 'posts/detail.html', context)

def update(request, post_pk):
    post = get_object_or_404(Post, pk=post_pk)  # 수정할 글을 가져오기 위해
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
    if request.method == 'POST':
        post.delete()
    return redirect('posts:list')
    # else:
    #     return redirect('posts:detail', post.pk)