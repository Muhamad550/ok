from rest_framework import serializers
from .models import Article, Topic, Review
from django.contrib.auth.models import User

class TopicSerializer(serializers.ModelSerializer):
    class Meta:
        model = Topic
        fields = ['id', 'name']

class ArticleSerializer(serializers.ModelSerializer):
    topic = TopicSerializer(read_only=True)
    topic_id = serializers.PrimaryKeyRelatedField(
        queryset=Topic.objects.all(), 
        source='topic', 
        write_only=True
    )
    author = serializers.ReadOnlyField(source='author.username')

    class Meta:
        model = Article
        fields = ['id', 'title', 'slug', 'content', 'author', 'topic', 'topic_id', 'created_at', 'updated_at', 'is_published']

class ReviewSerializer(serializers.ModelSerializer):
    author = serializers.ReadOnlyField(source='user.username')
    article_title = serializers.ReadOnlyField(source='article.title')

    class Meta:
        model = Review
        fields = ['id', 'article', 'article_title', 'user', 'author', 'text', 'created_at']

class UserRegisterSerializer(serializers.Serializer):
    username = serializers.CharField()
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)
    password_confirmation = serializers.CharField(write_only=True)

class UserLoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()

class UserLogoutSerializer(serializers.Serializer):
    confirm_logout = serializers.BooleanField(default=False)

class ArticleDeleteSerializer(serializers.Serializer):
    confirm_deletion = serializers.BooleanField(default=False)