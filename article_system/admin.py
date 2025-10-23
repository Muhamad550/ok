from django.contrib import admin
from .models import Article, Topic, Review

@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ['title', 'author', 'created_at', 'is_published']
    list_filter = ['is_published', 'topic']
    search_fields = ['title', 'content']

@admin.register(Topic)
class TopicAdmin(admin.ModelAdmin):
    list_display = ['name']

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ['article', 'user', 'created_at']