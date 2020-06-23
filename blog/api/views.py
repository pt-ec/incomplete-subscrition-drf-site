from rest_framework import viewsets, generics, permissions
from rest_framework.filters import OrderingFilter, SearchFilter

from core.api.permissions import IsAdminUserOrReadOnly, IsOwnerOrReadOnly
from core.api.pagination import CommentPagination, PostPagination
from blog.models import BlogPost
from profiles.models import Comment
from .serializers import BlogPostSerializer, CommentBlogPostSerializer


class BlogPostViewSet(viewsets.ModelViewSet):
    """ Blog Post CRUD View set """
    queryset = BlogPost.objects.filter(visible=True)
    serializer_class = BlogPostSerializer
    permission_classes = (IsAdminUserOrReadOnly,)
    filter_backends = (SearchFilter, OrderingFilter,)
    search_fields = ('title', 'description', 'author')
    ordering_fields = ('title', 'created_at', 'written_at')
    ordering = ('-written_at',)
    pagination_class = PostPagination


class BlogPostCommentCreateAPIView(generics.CreateAPIView):
    """ Create a comment in a blog post """
    queryset = Comment.objects.all()
    serializer_class = CommentBlogPostSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def perform_create(self, serializer):
        blog_post_pk = self.kwargs.get('blog_post_pk')
        blog_post = get_object_or_404(BlogPost, pk=blog_post_pk)
        user = self.request.user

        serializer.save(user=user, blog_post=blog_post)


class BlogPostCommentListAPIView(generics.ListAPIView):
    """ List comments in a blog post """
    serializer_class = CommentBlogPostSerializer
    permissions_class = (IsOwnerOrReadOnly,)
    pagination_class = CommentPagination

    def get_queryset(self):
        blog_post_pk = self.kwargs.get('blog_post_pk')
        blog_post = get_object_or_404(BlogPost, pk=blog_post_pk)
        return blog_post.comments.all().order_by('-created_at')


class BlogPostCommentDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    """ Retrieve update destroy comment this Video """
    queryset = Comment.objects.all()
    serializer_class = CommentBlogPostSerializer
    permission_classes = (IsOwnerOrReadOnly,)
