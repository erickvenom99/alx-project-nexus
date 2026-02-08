from rest_framework import permissions

class IsSellerOrReadOnly(permissions.BasePermission):
    """
    Custom permission to only allow sellers to create products.
    """
    def has_permission(self, request, view):
        # Allow anyone to perform "Read-only" actions (GET, HEAD, OPTIONS)
        if request.method in permissions.SAFE_METHODS:
            return True
        
        # Check if user is logged in and is a seller (or admin)
        return bool(
            request.user and 
            request.user.is_authenticated and 
            (request.user.role == 'seller' or request.user.is_staff)
        )

class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    Object-level permission to only allow owners of a product to edit it.
    """
    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to any request
        if request.method in permissions.SAFE_METHODS:
            return True

        # Instance must have an attribute named `seller`
        return obj.seller == request.user