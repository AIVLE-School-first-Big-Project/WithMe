import os
from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from .models import Post, Reply
from .forms import PostForm
from accounts.models import User
from django.db.models import Q
import json
from uuid import uuid4
from django.utils import timezone


def uuid_name_upload_to(filename):
    ymd_path = timezone.now().strftime('%Y/%m/%d')
    uuid_name = uuid4().hex
    extension = os.path.splitext(filename)[-1].lower()  # 확장자 추출하고, 소문자로 변환
    return '/'.join([
        ymd_path,
        uuid_name[:2],
        uuid_name + extension,
    ])


# Create your views here.
@login_required
def bulletin(request):
    # 입력 파라미터
    page = int(request.GET.get('page', 1))
    keyword = request.GET.get('keyword', '')

    # 게시판 (등록일 기준 최신 순)
    post_list = Post.objects.all().order_by('-write_date')

    # 검색 기능
    if keyword:
        post_list = post_list.filter(
            Q(title__icontains=keyword) | Q(content__icontains=keyword) | Q(user__username__icontains=keyword)
        ).distinct()

    # 한 페이지 당 5개 게시물
    post_count = 5
    paginator = Paginator(post_list, post_count)
    print_range = 5
    start_page = (page - 1) // print_range * print_range + 1
    end_page = min(start_page + (print_range - 1), paginator.num_pages)
    post_obj = paginator.get_page(page)
    context = {'post_list': post_obj, 'current_page': page, 'keyword': keyword,
               'page_range': range(start_page, end_page + 1)}

    return render(request, 'bulletin/main.html', context)


@login_required
def post(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    reply_list = Reply.objects.filter(post__id=post_id)
    if request.method == "POST":
        reply = Reply()
        reply.post = Post.objects.get(id=post_id)
        reply.user = request.user
        reply.content = request.POST.get('content')
        reply.created_at = timezone.now()
        if reply.content != '':
            reply.save()

    return render(request, 'bulletin/post.html', {'post': post, 'reply_list': reply_list})


@login_required
def upload_post(request):
    if request.method == "POST":
        print("request:", request)
        post = Post()
        post.title = request.POST['title']
        post.content = request.POST['content']
        try:
            post.image = request.FILES['image']
            post.image.name = uuid_name_upload_to(post.image.name)
            print(post.image.name)
        except ValueError:
            print("\n" * 10)
            print("error")
            print("\n" * 10)

        post.write_date = timezone.now()
        post.user = request.user
        post.save()
        return redirect("../")
    else:
        form = PostForm()

    return render(request, 'bulletin/upload_post.html', {'form': form})


@login_required
def modify_post(request, post_id):
    login_session = request.session.get('login_session', '')
    context = {'login_session': login_session}

    post = Post.objects.get(id=post_id)

    if request.method == "POST":
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            post = form.save(commit=False)
            post.modify_date = timezone.now()

            post.save()
            return redirect('/bulletin/' + str(post.id), context)
    else:
        form = PostForm(instance=post)

    context = {'form': form}
    return render(request, 'bulletin/modify_post.html', context)


@login_required
def delete_post(request, post_id):
    post = Post.objects.get(id=post_id)
    post.delete()
    return redirect('/bulletin')


@login_required
def add_reply(request):
    obj = request.body.decode("utf-8")
    data = json.loads(obj)

    post_id = data['post_id']
    user_id = data['user_id']
    content = data['content']
    if request.method == "POST":
        reply = Reply()
        reply.post = Post.objects.get(id=post_id)
        reply.user = User.objects.get(id=user_id)
        reply.content = content
        reply.created_at = timezone.now()
        if reply.content != '':
            print(reply.content)
            reply.save()

    return JsonResponse(data)


@login_required
def delete_reply(request):
    obj = request.body.decode("utf-8")
    data = json.loads(obj)

    reply_id = data['reply_id']

    target = Reply.objects.get(id=reply_id)
    target.delete()

    return JsonResponse(data)
