from rest_framework import pagination, serializers

from subscription_classes.models import (VideoClass, Video,
                                         VideoClassSection)
from profiles.models import Comment, Review
from profiles.api.serializers import (CommentSerializer,
                                      ReviewSerializer)


class VideoSerializer(serializers.ModelSerializer):
    """ Video model serializer """
    comments = serializers.SerializerMethodField('paginated_comments')

    class Meta:
        model = Video
        fields = '__all__'
        read_only_fields = ('created_at', 'edited_at')

    def paginated_comments(self, obj):
        paginator = pagination.PageNumberPagination()
        page = paginator.paginate_queryset(
            Video.objects.all(),
            self.context['request'])
        serializer = CommentSerializer(
            page, many=True,
            context={'request': self.context['request']})
        return serializer.data


class VideoClassSectionSerializer(serializers.ModelSerializer):
    """ Video class model serializer """
    videos = serializers.HyperlinkedRelatedField(
        many=True,
        read_only=True)

    class Meta:
        model = VideoClassSection
        fields = '__all__'
        read_only_fields = ('created_at', 'edited_at')


class VideoClassSerializer(serializers.ModelSerializer):
    """ Video Class Serializer """
    sections = VideoClassSectionSerializer(read_only=True,
                                           many=True)
    reviews = serializers.SerializerMethodField('paginated_reviews')

    class Meta:
        model = VideoClass
        fields = '__all__'
        read_only_fields = ('created_at', 'updated_at',
                            'subscription_plans')

    def paginated_reviews(self, obj):
        paginator = pagination.PageNumberPagination()
        page = paginator.paginate_queryset(
            Review.objects.all(),
            self.context['request'])
        serializer = ReviewSerializer(
            page, many=True,
            context={'request': self.context['request']})
        return serializer.data


class VideoClassReviewSerializer(ReviewSerializer):
    """ Serializer to add a review to a video class """

    def create(self, validated_data):
        video_class = validated_data.pop('video_class')
        review = Review.objects.create(**validated_data)
        video_class.reviews.add(review)
        return review


class VideoCommentSerializer(CommentSerializer):
    """ Serializer to add a comment to a video """

    def create(self, validated_data):
        video = validated_data.pop('video')
        comment = Comment.objects.create(**validated_data)
        video.comments.add(comment)
        return comment
