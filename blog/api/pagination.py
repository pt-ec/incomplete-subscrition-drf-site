from rest_framework.pagination import PageNumberPagination


class BlogPagination(PageNumberPagination):
    page_size = 5
    page_query_param = 'blog_page'
    page_size_query_param = 'blog_page_size'
    max_page_size = 100
