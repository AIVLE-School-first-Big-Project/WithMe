# from django.shortcuts import render

# # Create your views here.

from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.core.paginator import Paginator
from .models import BulletinFeed
from .forms import BulletinFeedForm
from django.utils import timezone

# Create your views here.

def board(request):
    # 게시판 (등록일 기준 최신 순- id desc)
    feeds = BulletinFeed.objects.all().order_by('-id')
    # query param 으로 넘어오는 page 값
    current_page      = int(request.GET.get('page', 1))
    # 한 페이지 당 5개 피드
    feed_count = 5
    paginator  = Paginator(feeds, feed_count)
    
    last_page = paginator.num_pages

    # 최대페이지보다 클 경우 요청 페이지를 마지막 페이지로
    current_page = min(current_page, last_page)

    # 출력 범위 설정
    print_range = 5
    start_page = (current_page - 1) // print_range * print_range + 1
    end_page = min(start_page + (print_range - 1), last_page)
    
    board = paginator.page(current_page)
    context = {'board':board,  'board_number' : current_page, 'page_range' : range(start_page, end_page + 1),}

    return render(request, 'bulletin/board.html', context)

def feed(request, feed_id):
    # feed = BulletinFeed.objects.get(id = feed_id)
    feed = get_object_or_404(BulletinFeed, id = feed_id)
    return render(request, 'bulletin/feed.html', {'feed':feed})

def upload(request):
    if request.method == "POST":
        form = BulletinFeedForm(request.POST)
        if form.is_valid():
            feed = form.save(commit=False)
            feed.upload_time = timezone.now()
            feed.save()
            return redirect("../")
    else:
        form = BulletinFeedForm()
    return render(request, 'bulletin/upload.html', {'form':form})