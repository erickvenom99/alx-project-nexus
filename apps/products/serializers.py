from rest_framework import serializers
from .models import Product, Category

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name', 'slug', 'description']

class ProductSerializer(serializers.ModelSerializer):
    # Instead of just showing category ID (e.g., "1"), show the actual name (e.g., "Electronics")
    # We use SlugRelatedField for this, or we could nest the whole CategorySerializer
    category = serializers.SlugRelatedField(
        slug_field='slug', 
        queryset=Category.objects.all()
    )
    
    class Meta:
        model = Product
        fields = [
            'id', 'category', 'name', 'slug', 'description', 
            'price', 'stock', 'image', 'is_active', 'created_at'
        ]