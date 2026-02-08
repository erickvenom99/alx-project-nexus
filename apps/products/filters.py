from django_filters import rest_framework as filters
from .models import Product

class ProductFilter(filters.FilterSet):
    # Define price range filters
    min_price = filters.NumberFilter(field_name="price", lookup_expr='gte')
    max_price = filters.NumberFilter(field_name="price", lookup_expr='lte')
    
    # Allow searching by category slug or name
    category = filters.CharFilter(field_name="category__slug")

    class Meta:
        model = Product
        fields = ['category', 'min_price', 'max_price', 'is_active']