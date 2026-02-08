from rest_framework import generics, filters as drf_filters
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.permissions import AllowAny
from .models import Category, Product
from .serializers import CategorySerializer, ProductSerializer
from .filters import ProductFilter
from .pagination import ProductPagination
from .permissions import IsSellerOrReadOnly, IsOwnerOrReadOnly

class ProductListView(generics.ListCreateAPIView):
    """View to list all active products"""
    queryset = Product.objects.filter(is_active=True)
    filter_backends = [DjangoFilterBackend, drf_filters.SearchFilter, drf_filters.OrderingFilter]
    filterset_class = ProductFilter
    pagination_class = ProductPagination
    search_fields = ['name', 'description']
    
    # Allow users to sort by price or date
    ordering_fields = ['price', 'created_at']
    serializer_class = ProductSerializer
    permission_classes = [IsSellerOrReadOnly]
    def perform_create(self, serializer):
        # Automatically set the seller to the logged-in user
        serializer.save(seller=self.request.user)

class ProductDetailView(generics.RetrieveUpdateDestroyAPIView):
    """View to get a single product by its slug"""
    queryset = Product.objects.filter(is_active=True)
    serializer_class = ProductSerializer
    lookup_field = 'slug'
    permission_classes = [IsSellerOrReadOnly, IsOwnerOrReadOnly]