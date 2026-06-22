from .models import Cart


def cart_summary(request):
    """Makes `cart_item_count` available in every template (navbar badge)."""
    if request.user.is_authenticated:
        cart = Cart.objects.filter(user=request.user).first()
        count = cart.total_quantity if cart else 0
    else:
        count = 0
    return {'cart_item_count': count}
