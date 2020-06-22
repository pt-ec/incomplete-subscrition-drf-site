from rest_framework.pagination import PageNumberPagination


class ItemPagination(PageNumberPagination):
    page_size = 9
    page_query_param = 'item_page'


class ReviewPagination(PageNumberPagination):
    page_size = 10
    page_query_param = 'review_page'
    page_size_query_param = 'review_page_size'
    max_page_size = 50


class CommentPagination(PageNumberPagination):
    page_size = 10
    page_query_param = 'comment_page'
    page_size_query_param = 'comment_page_size'
    max_page_size = 100
