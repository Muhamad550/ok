from rest_framework import generics, permissions, status, filters
from rest_framework.response import Response
from rest_framework.exceptions import PermissionDenied
from rest_framework.pagination import PageNumberPagination
from django_filters.rest_framework import DjangoFilterBackend
from .models import BlogPost, Category, Comment
from .serializers import BlogPostSerializer, CategorySerializer, CommentSerializer, LoginSerializer, RegisterSerializer, LogoutSerializer, DeleteBlogPostSerializer
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from rest_framework.renderers import BrowsableAPIRenderer, JSONRenderer
from rest_framework.authtoken.models import Token
from django.shortcuts import redirect
from django.urls import reverse
from django.http import HttpResponseRedirect



# Pagination Setup
class BlogPostPagination(PageNumberPagination):
    page_size = 10


# BlogPost Views
class BlogPostListCreateView(generics.ListCreateAPIView):
    """
    View to list all blog posts or create a new post.
    """
    queryset = BlogPost.objects.filter(status='published')
    serializer_class = BlogPostSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    pagination_class = BlogPostPagination
    filter_backends = [filters.SearchFilter, DjangoFilterBackend]
    search_fields = ['title', 'content']
    filterset_fields = ['category', 'author']

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class BlogPostDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    View to retrieve, update, or delete a specific blog post.
    """
    queryset = BlogPost.objects.all()
    serializer_class = BlogPostSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    lookup_field = 'slug'  # ✅ This line ensures it works with slugs

    def perform_update(self, serializer):
        if serializer.instance.author != self.request.user:
            raise PermissionDenied("You can only edit your own posts.")
        serializer.save()

    def delete(self, request, *args, **kwargs):
        """
        Override DELETE to show a confirmation form for the browsable API.
        """
        serializer = DeleteBlogPostSerializer(data=request.data)
        if serializer.is_valid() and serializer.validated_data['confirm_delete']:
            self.perform_destroy(self.get_object())
            # ✅ Redirect back to the blog posts list after deletion in the HTML view
            if request.accepted_renderer.format == 'html':
                return HttpResponseRedirect(reverse('blog:post-list-create'))
            return Response({'message': 'Blog post deleted successfully.'}, status=status.HTTP_204_NO_CONTENT)
        return Response({'error': 'Please confirm deletion.'}, status=status.HTTP_400_BAD_REQUEST)    


# Category Views
class CategoryListView(generics.ListAPIView):
    """
    View to list all categories.
    """
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [permissions.AllowAny]


class PostsByCategoryView(generics.ListAPIView):
    """
    View to list posts by category.
    """
    serializer_class = BlogPostSerializer

    def get_queryset(self):
        category_id = self.kwargs.get('category_id')
        return BlogPost.objects.filter(category__id=category_id, status='published')


# Comment Views
class CommentListCreateView(generics.ListCreateAPIView):
    """
    View to list or create comments for a blog post.
    """
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        post_id = self.kwargs.get('post_id')
        return Comment.objects.filter(post__id=post_id)

    def perform_create(self, serializer):
        serializer.save(author=self.request.user, post_id=self.kwargs.get('post_id'))


class CommentDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    View to retrieve, update, or delete a specific comment.
    """
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def perform_update(self, serializer):
        if serializer.instance.author != self.request.user:
            raise PermissionDenied("You can only edit your own comments.")
        serializer.save()

    def perform_destroy(self, instance):
        # Ensure only the author can delete the comment
        if instance.author != self.request.user:
            raise PermissionDenied("You can only delete your own comments.")
        instance.delete()


class RegisterView(APIView):
    permission_classes = [AllowAny]
    serializer_class = RegisterSerializer
    renderer_classes = [BrowsableAPIRenderer, JSONRenderer]

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            username = serializer.validated_data['username']
            email = serializer.validated_data['email']
            password = serializer.validated_data['password']
            confirm_password = serializer.validated_data['confirm_password']

            if password != confirm_password:
                return Response({'error': 'Passwords do not match.'}, status=status.HTTP_400_BAD_REQUEST)

            if User.objects.filter(username=username).exists():
                return Response({'error': 'Username already exists.'}, status=status.HTTP_400_BAD_REQUEST)
            
            # Create user and redirect to login page
            user = User.objects.create_user(username=username, email=email, password=password)
            token, _ = Token.objects.get_or_create(user=user)

            # Redirect only if it's the Browsable API (HTML)
            if request.accepted_renderer.format == 'html':
                return redirect(reverse('blog:login'))  # Redirect to the login page
            
            # If it's an API request (JSON response)
            return Response({'message': 'User registered successfully. Please log in', 'token': token.key}, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



class LoginView(APIView):
    permission_classes = [AllowAny]
    serializer_class = LoginSerializer
    renderer_classes = [BrowsableAPIRenderer, JSONRenderer]  # Important for form fields to show

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            username = serializer.validated_data['username']
            password = serializer.validated_data['password']

            user = authenticate(username=username, password=password)
            if user:
                # Token Authentication (for APIs)
                token, _ = Token.objects.get_or_create(user=user)

                 # Session Authentication (for Browsable API)
                login(request, user)  # Logs the user into the session

                return Response({'message': 'Login successful.', 'token': token.key}, status=status.HTTP_200_OK)
            return Response({'error': 'Invalid credentials.'}, status=status.HTTP_401_UNAUTHORIZED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



class LogoutView(APIView):
    """
    View to log out a user by deleting their authentication token.
    """
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = LogoutSerializer
    renderer_classes = [BrowsableAPIRenderer, JSONRenderer]

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            try:
                 # Clear token-based authentication
                request.user.auth_token.delete()

                # Clear session-based authentication for the browsable API
                logout(request)
                
                return Response({'message': 'Logout successful.'}, status=status.HTTP_200_OK)
            except AttributeError:
                return Response({'error': 'You are not logged in.'}, status=status.HTTP_400_BAD_REQUEST)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
