from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import Cart, CartItem
from .serializers import CartSerializer, CartItemSerializer

class CartDetailView(generics.RetrieveAPIView):
    """
    View to see the current user's cart.
    """
    serializer_class = CartSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        # Always return the cart belonging to the logged-in user
        return self.request.user.cart

class AddToCartView(generics.CreateAPIView):
    """
    View to add items to the cart.
    """
    serializer_class = CartItemSerializer
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        cart = request.user.cart
        product_id = request.data.get('product_id')
        quantity = int(request.data.get('quantity', 1))

        # Check if item exists, update quantity if it does, else create
        item, created = CartItem.objects.get_or_create(
            cart=cart, 
            product_id=product_id
        )
        
        if not created:
            item.quantity += quantity
        else:
            item.quantity = quantity
        
        item.save()
        return Response(CartSerializer(cart).data, status=status.HTTP_201_CREATED)