from rest_framework import serializers

from blog.models import BlogPost
from profiles.models import Comment
from profiles.api.serializers import CommentSerializer


class BlogPostSerializer(serializers.ModelSerializer):
    """ Blog Post Model Serializer """

    class Meta:
        model = BlogPost
        exclude = ('comments',)
        read_only_fields = ('created_at', 'updated_at')


class CommentBlogPostSerializer(CommentSerializer):
    """ Blog post comment serializer """

    def create(self, validated_data):
        blog_post = validated_data.pop('blog_post')
        comment = Comment.objects.create(**validated_data)
        blog_post.comments.add(comment)
        return comment
