from rest_framework import serializers
from .models import BlogPost, Category, Comment
from django.contrib.auth.models import User

# User Serializer
class UserSerializer(serializers.ModelSerializer):
    """
    Serializer for User model to display limited user information.
    """
    class Meta:
        model = User
        fields = ['id', 'username', 'email']


# Category Serializer
class CategorySerializer(serializers.ModelSerializer):
    """
    Serializer for Category model.
    """
    class Meta:
        model = Category
        fields = [ 'name']


# Comment Serializer
class CommentSerializer(serializers.ModelSerializer):
    """
    Serializer for Comment model.
    Includes nested representation of the author.
    """
    author = UserSerializer(read_only=True)

    class Meta:
        model = Comment
        fields = ['id', 'post', 'author', 'content', 'created_at', 'updated_at']


# BlogPost Serializer
class BlogPostSerializer(serializers.ModelSerializer):
    """
    Serializer for BlogPost model.
    Includes nested representation of the author and category.
    """
    author = UserSerializer(read_only=True)
    category = CategorySerializer(read_only=True)
    category_id = serializers.PrimaryKeyRelatedField(
        queryset=Category.objects.all(),
        source='category',
        write_only=True
    )
    liked_by = UserSerializer(many=True, read_only=True)  # Display users who liked the post
    comments = CommentSerializer(many=True, read_only=True)  # Nested comments
    is_liked = serializers.SerializerMethodField()

    class Meta:
        model = BlogPost
        fields = [
            'id', 'title', 'slug', 'content', 'author', 'category', 'category_id',
            'status', 'created_at', 'updated_at', 'liked_by', 'is_liked', 'comments'
        ]

    def get_is_liked(self, obj):
        """
        Check if the current user has liked this post.
        """
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            return obj.liked_by.filter(id=request.user.id).exists()
        return False

    def create(self, validated_data):
        """
        Overriding create method to allow assigning a category during post creation.
        """
        category = validated_data.pop('category', None)
        post = BlogPost.objects.create(**validated_data)
        if category:
            post.category = category
            post.save()
        return post
    
class DeleteBlogPostSerializer(serializers.Serializer):
    confirm_delete = serializers.BooleanField(default=False, help_text="Check to confirm deletion.")


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=150)
    password = serializers.CharField(write_only=True, style={'input_type': 'password'})


class RegisterSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=150)
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True, style={'input_type': 'password'})
    confirm_password = serializers.CharField(write_only=True, style={'input_type': 'password'})

    
class LogoutSerializer(serializers.Serializer):
    confirm_logout = serializers.BooleanField(default=True, help_text="Click 'Submit' to confirm logout.")

