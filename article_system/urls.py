from django.urls import path
from . import views

app_name = 'content'

urlpatterns = [
    path('articles/', views.ArticleListCreateView.as_view(), name='article-list'),
    path('articles/<slug:slug>/', views.ArticleDetailView.as_view(), name='article-detail'),
    path('topics/', views.TopicListView.as_view(), name='topic-list'),
    path('topics/<int:topic_id>/articles/', views.ArticlesByTopicView.as_view(), name='articles-by-topic'),
    path('articles/<int:article_id>/reviews/', views.ReviewListCreateView.as_view(), name='review-list'),
    path('reviews/<int:pk>/', views.ReviewDetailView.as_view(), name='review-detail'),
    path('register/', views.UserRegisterView.as_view(), name='user-register'),
    path('login/', views.UserLoginView.as_view(), name='user-login'),
    path('logout/', views.UserLogoutView.as_view(), name='user-logout'),
]