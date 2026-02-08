from rest_framework import generics, filters as drf_filters
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.permissions import AllowAny
from .models import Category, Product
from .serializers import CategorySerializer, ProductSerializer
from .filters import ProductFilter
from .pagination import ProductPagination
from .permissions import IsSellerOrReadOnly, IsOwnerOrReadOnly
from drf_spectacular.utils import extend_schema, extend_schema_view, OpenApiParameter
from drf_spectacular.types import OpenApiTypes

@extend_schema_view(
    list=extend_schema(
        summary="List all products",
        description="Retrieve a paginated list of all available products. Supports filtering by category and sorting by price.",
        parameters=[
            OpenApiParameter(
                name="category",
                type=OpenApiTypes.INT,
                location=OpenApiParameter.QUERY,
                description="Filter by Category ID (e.g., ?category=1)"
            ),
            OpenApiParameter(
                name="ordering",
                type=OpenApiTypes.STR,
                location=OpenApiParameter.QUERY,
                description="Sort results. Use 'price' for ascending or '-price' for descending."
            ),
        ]
    ),
    retrieve=extend_schema(
        summary="Get product details",
        description="Returns full details for a single product ID."
    ),
)
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

@extend_schema(responses=ProductSerializer, auth=[{'BearerAuth': []}])
def create(self, request, *args, **kwargs):
    return super().create(request, *args, **kwargs)