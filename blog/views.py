from rest_framework import generics, permissions, status, filters
from rest_framework.response import Response
from rest_framework.exceptions import PermissionDenied
from rest_framework.pagination import PageNumberPagination
from django_filters.rest_framework import DjangoFilterBackend
from .models import Article, Topic, Review
from .serializers import ArticleSerializer, TopicSerializer, ReviewSerializer, UserLoginSerializer, UserRegisterSerializer, UserLogoutSerializer, ArticleDeleteSerializer
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from rest_framework.renderers import BrowsableAPIRenderer, JSONRenderer
from rest_framework.authtoken.models import Token
from django.shortcuts import redirect
from django.urls import reverse
from django.http import HttpResponseRedirect


class ArticlePagination(PageNumberPagination):
    page_size = 12


class ArticleListCreateView(generics.ListCreateAPIView):
    queryset = Article.objects.filter(is_published=True)
    serializer_class = ArticleSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    pagination_class = ArticlePagination
    filter_backends = [filters.SearchFilter, DjangoFilterBackend]
    search_fields = ['title', 'content']
    filterset_fields = ['topic', 'author']

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class ArticleDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    lookup_field = 'slug'

    def perform_update(self, serializer):
        if serializer.instance.author != self.request.user:
            raise PermissionDenied("You can only modify your own articles.")
        serializer.save()

    def delete(self, request, *args, **kwargs):
        delete_serializer = ArticleDeleteSerializer(data=request.data)
        if delete_serializer.is_valid() and delete_serializer.validated_data['confirm_deletion']:
            self.perform_destroy(self.get_object())
            if request.accepted_renderer.format == 'html':
                return HttpResponseRedirect(reverse('content:article-list'))
            return Response({'message': 'Article removed successfully.'}, status=status.HTTP_204_NO_CONTENT)
        return Response({'error': 'Deletion confirmation required.'}, status=status.HTTP_400_BAD_REQUEST)


class TopicListView(generics.ListAPIView):
    queryset = Topic.objects.all()
    serializer_class = TopicSerializer
    permission_classes = [permissions.AllowAny]


class ArticlesByTopicView(generics.ListAPIView):
    serializer_class = ArticleSerializer

    def get_queryset(self):
        topic_id = self.kwargs.get('topic_id')
        return Article.objects.filter(topic__id=topic_id, is_published=True)


class ReviewListCreateView(generics.ListCreateAPIView):
    serializer_class = ReviewSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        article_id = self.kwargs.get('article_id')
        return Review.objects.filter(article__id=article_id)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user, article_id=self.kwargs.get('article_id'))


class ReviewDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def perform_update(self, serializer):
        if serializer.instance.user != self.request.user:
            raise PermissionDenied("You can only modify your own reviews.")
        serializer.save()

    def perform_destroy(self, instance):
        if instance.user != self.request.user:
            raise PermissionDenied("You can only remove your own reviews.")
        instance.delete()


class UserRegisterView(APIView):
    permission_classes = [AllowAny]
    serializer_class = UserRegisterSerializer
    renderer_classes = [BrowsableAPIRenderer, JSONRenderer]

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            username = serializer.validated_data['username']
            email = serializer.validated_data['email']
            password = serializer.validated_data['password']
            password_confirmation = serializer.validated_data['password_confirmation']

            if password != password_confirmation:
                return Response({'error': 'Password confirmation does not match.'}, status=status.HTTP_400_BAD_REQUEST)

            if User.objects.filter(username=username).exists():
                return Response({'error': 'Username is already taken.'}, status=status.HTTP_400_BAD_REQUEST)
            
            user_account = User.objects.create_user(username=username, email=email, password=password)
            auth_token, _ = Token.objects.get_or_create(user=user_account)

            if request.accepted_renderer.format == 'html':
                return redirect(reverse('content:user-login'))
            
            return Response({
                'message': 'Account created successfully. Please sign in.',
                'token': auth_token.key
            }, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserLoginView(APIView):
    permission_classes = [AllowAny]
    serializer_class = UserLoginSerializer
    renderer_classes = [BrowsableAPIRenderer, JSONRenderer]

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            username = serializer.validated_data['username']
            password = serializer.validated_data['password']

            user = authenticate(username=username, password=password)
            if user:
                auth_token, _ = Token.objects.get_or_create(user=user)
                login(request, user)

                return Response({
                    'message': 'Sign in successful.',
                    'token': auth_token.key
                }, status=status.HTTP_200_OK)
            return Response({'error': 'Invalid login credentials.'}, status=status.HTTP_401_UNAUTHORIZED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserLogoutView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = UserLogoutSerializer
    renderer_classes = [BrowsableAPIRenderer, JSONRenderer]

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            try:
                request.user.auth_token.delete()
                logout(request)
                
                return Response({'message': 'Signed out successfully.'}, status=status.HTTP_200_OK)
            except AttributeError:
                return Response({'error': 'No active session found.'}, status=status.HTTP_400_BAD_REQUEST)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)