# blog/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.post_list, name='post_list'),
    path('posts/<int:pk>/', views.post_detail, name='post_detail'),
    path('register/', views.register, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('posts/new/', views.post_create, name='post_create'),
    path('posts/<int:pk>/comment/', views.add_comment, name='add_comment'),
    path('posts/<int:pk>/edit/', views.post_edit, name='post_edit'),
    path('posts/<int:pk>/delete/', views.post_delete, name='post_delete'),
    path('like/<int:pk>', views.like_post, name='like_post'),
    path('comment/<int:pk>/delete/', views.comment_delete, name='comment_delete'),
]
