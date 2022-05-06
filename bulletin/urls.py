from django.urls import path
from . import views

app_name = 'bulletin'
urlpatterns = [
    # 기본 페이지
    path('', views.board, name='board'),
    # 해당 feed_id 게시글
    path('<int:feed_id>/', views.feed),
    # 글쓰기
    path('upload/', views.upload, name='upload'),
]