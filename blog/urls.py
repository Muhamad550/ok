from django.urls import path
from .views import (
    BlogPostListCreateView,
    BlogPostDetailView,
    CategoryListView,
    PostsByCategoryView,
    CommentListCreateView,
    CommentDetailView,
    RegisterView, LoginView, LogoutView
)

app_name = 'blog'  # Set this to match the namespace in your project-level urls.py

urlpatterns = [
    path('posts/', BlogPostListCreateView.as_view(), name='post-list-create'),
    path('posts/<slug:slug>/', BlogPostDetailView.as_view(), name='post-detail'),
    path('categories/', CategoryListView.as_view(), name='category-list'),
    path('categories/<int:category_id>/posts/', PostsByCategoryView.as_view(), name='posts-by-category'),
    path('posts/<int:post_id>/comments/', CommentListCreateView.as_view(), name='comment-list-create'),
    path('comments/<int:pk>/', CommentDetailView.as_view(), name='comment-detail'),
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
]
