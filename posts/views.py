from django.shortcuts import render, redirect, get_list_or_404, get_object_or_404
from .models import Post, Image, Comment, Hashtag
from .forms import PostForm, ImageForm, CommentForm
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.db.models import Q
from itertools import chain

# Create your views here.
@login_required
def list(request):
    # 1
    followings = request.user.followings.all()
    posts = Post.objects.filter(Q(user__in=followings) | Q(user=request.user.id)).order_by('-pk')
    
    # 2
    # followings = request.user.followings.all()
    # chain_followings = chain(followings, [request.user])
    # posts = Post.objects.filter(user__in=chain_followings).order_by('-pk')
    
    
    
    # posts = Post.objects.filter(user__in=request.user.followings.all()).order_by('-pk')   # 팔로잉 글
    # posts = get_list_or_404(Post.objects.order_by('-pk'))     # 모든 글
    comment_form = CommentForm()
    context = {
        'posts': posts,
        'comment_form': comment_form,
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
            # hashtag - post.save()가 된 이후에 hashtag 코드가 와야함
            # 1. 게시글을 순회하면서 띄어쓰기를 잘라야 함
            # 2. 자른 단어가 #으로 시작하나?
            # 3. 이 해시태그가 기존 해시태그에 있는건지?
            
            for word in post.content.split():
                if word[0] == '#':
                # if word.startswith('#'):
                    hashtag = Hashtag.objects.get_or_create(content=word)
                    post.hashtags.add(hashtag[0])
                    # (모델객체의 인스턴스, BOOLEAN)을 리턴 
                    # ex) 없으면 새로 생성 : (hashtag, True), 있으면 : (hashtag, False)
                    
                    # hashtag, new = Hashtag.objects.get_or_create(content=word)
                    # if new:
                    #     post.hashtags.add(hashtag)
                    
            # contents = post.content.split()
            # for content in contents:
            #     if content[0] == '#':
            #         hashtag = Hashtag.objects.create(content=content)
            #     post.hashtags.add(hashtag)
            
            
            
            
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
            # post_form.save()
            post = post_form.save()
            # hashtag update
            post.hashtags.clear()
            for word in post.content.split():
                if word[0] == '#':
                    hashtag = Hashtag.objects.get_or_create(content=word)
                    post.hashtags.add(hashtag[0])
            
            
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

@login_required
@require_POST
def comment_create(request, post_pk):
    form = CommentForm(request.POST)
    if form.is_valid():
        comment = form.save(commit=False)
        comment.user = request.user
        comment.post_id = post_pk
        comment.save()
    return redirect('posts:list')

@login_required
@require_POST
def comment_delete(request, post_pk, comment_pk):
    comment = get_object_or_404(Comment, pk=comment_pk)
    if request.user != comment.user:
        return redirect('posts:list')
    comment.delete()
    return redirect('posts:list')
    
@login_required
def like(request, post_pk):
    post = get_object_or_404(Post, pk=post_pk)
    # 이미 해당 유저가 like_users에 존재하면 해당 유저를 삭제
    # (이미 해당 유저가 like를 누른 상태면 좋아요 취소)
    if request.user in post.like_users.all():
        post.like_users.remove(request.user)   
    else:   # 없으면 추가(좋아요)
        post.like_users.add(request.user)
    return redirect('posts:list')
    
    # 2
    # user = request.user
    # if post.like_users.filter(pk=user.pk).exists():
    #     post.like_users.remove()
    # else:
    #     post.like_users.add(user)
    # return redirect('posts:list')
    
@login_required
def explore(request):
    # posts = Post.objects.order_by('-pk')
    posts = Post.objects.exclude(user=request.user).order_by('-pk') # 내가 쓴 글 제외
    comment_form = CommentForm()
    context = {
        'posts': posts,
        'comment_form': comment_form,
    }
    return render(request, 'posts/explore.html', context)
    
    
def hashtag(request, hash_pk):
    hashtag = get_object_or_404(Hashtag, pk=hash_pk)
    posts = hashtag.post_set.order_by('-pk')
    context = {
        'hashtag': hashtag,
        'posts': posts,
    }
    return render(request, 'posts/hashtag.html', context)