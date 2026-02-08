from django.conf import settings
from django.db import models
from django.utils.text import slugify

class Category(models.Model): # Capitalized C
    """
    specify the group a product belongs to eg "electronics"
    """
    name = models.CharField(max_length=255, unique=True)
    slug = models.SlugField(max_length=255, unique=True, blank=True)
    description = models.TextField(blank=True)

    class Meta:
        verbose_name = "Category"
        verbose_name_plural = "Categories"
        ordering = ['name']
        indexes = [
            models.Index(fields=['name']),
            models.Index(fields=['slug']),
        ]
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

class Product(models.Model): # Fixed parentheses and capitalization
    """
    product available to users
    """
    category = models.ForeignKey(Category, related_name="products", on_delete=models.CASCADE)
    seller = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name="store_product",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )
    name = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, unique=True)
    description = models.TextField() # Fixed models plural
    
    # price usually needs decimal_places=2 for cents/kobo
    price = models.DecimalField(max_digits=10, decimal_places=2, db_index=True) 
    
    stock = models.PositiveIntegerField(default=0)
    image = models.ImageField(upload_to="product/", blank=True, null=True) # Fixed upload_to
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['price']),
            models.Index(fields=['category', 'price']),
            models.Index(fields=['is_active']), # Fixed field name to match model
            models.Index(fields=['created_at']),
        ]
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name