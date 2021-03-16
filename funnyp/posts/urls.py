from django.urls import path
from .views import (PostListView, PostDetailView, 
                    PostCreateView, PostUpdateView,
                    PostDeleteView, UserPostListView,
                    LikeView, UnlikeView, CategoryView)
from . import views

urlpatterns = [
    path('', PostListView.as_view(), name='blog-home'),
    path('post/new/', PostCreateView.as_view(), name='post-create'),
    path('user/<str:username>', UserPostListView.as_view(), name='user-posts'),
    path('post/<int:pk>/', PostDetailView.as_view(), name='post-detail'),
    path('like/<int:pk>', LikeView, name='like-post'),
    path('unlike/<int:pk>', UnlikeView, name='unlike-post'),
    path('post/<int:pk>/update/', PostUpdateView.as_view(), name='post-update'),
    path('post/<int:pk>/delete/', PostDeleteView.as_view(), name='post-delete'),
    path('category/<str:categories>', CategoryView, name='category'),
    
]