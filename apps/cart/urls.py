from django.urls import path
from .views import CartDetailView, AddToCartView

urlpatterns = [
    path('my-cart/', CartDetailView.as_view(), name='cart-detail'),
    path('add/', AddToCartView.as_view(), name='add-to-cart'),
]