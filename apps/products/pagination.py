from rest_framework.pagination import PageNumberPagination

class ProductPagination(PageNumberPagination):
    page_size = 12  # Number of products per page
    page_size_query_param = 'page_size' # Allow client to override (e.g., ?page_size=20)
    max_page_size = 100