from django.urls import path
from . import views

app_name = 'bulletin'
urlpatterns = [
    # 기본 페이지
    path('', views.bulletin, name='bulletin'),
    
    # 게시글 조회, 추가, 수정, 삭제
    path('<int:post_id>/', views.post),
    path('upload/', views.upload_post, name='upload_post'),
    path('<int:post_id>/modify/', views.modify_post, name='modify_post'),
    path('<int:post_id>/delete/', views.delete_post, name='delete_post'),
    
    # 댓글 추가, 삭제
    path('add_reply/', views.add_reply, name='add_reply'),
    path('delete_reply/', views.delete_reply, name='delete_reply'),

]