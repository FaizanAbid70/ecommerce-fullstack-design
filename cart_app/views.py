from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST

from products_app.models import Product
from .models import Cart, CartItem


def _get_cart(user):
    cart, _created = Cart.objects.get_or_create(user=user)
    return cart


@login_required
def cart_view(request):
    cart = _get_cart(request.user)
    context = {
        'cart': cart,
        'items': cart.active_items.select_related('product'),
        'saved_items': cart.saved_items.select_related('product'),
    }
    return render(request, 'cart_app/cart.html', context)


@login_required
@require_POST
def add_to_cart(request, pk):
    product = get_object_or_404(Product, pk=pk)
    cart = _get_cart(request.user)

    item, created = CartItem.objects.get_or_create(
        cart=cart, product=product, saved_for_later=False,
        defaults={'quantity': 1},
    )
    if not created:
        item.quantity += 1
        item.save()

    return redirect(request.POST.get('next') or 'cart')


@login_required
@require_POST
def update_quantity(request, item_id):
    item = get_object_or_404(CartItem, id=item_id, cart__user=request.user)
    try:
        qty = int(request.POST.get('quantity', 1))
    except ValueError:
        qty = 1
    item.quantity = max(1, qty)
    item.save()
    return redirect('cart')


@login_required
@require_POST
def remove_item(request, item_id):
    item = get_object_or_404(CartItem, id=item_id, cart__user=request.user)
    item.delete()
    return redirect('cart')


@login_required
@require_POST
def remove_all(request):
    cart = _get_cart(request.user)
    cart.active_items.delete()
    return redirect('cart')


@login_required
@require_POST
def save_for_later(request, item_id):
    item = get_object_or_404(CartItem, id=item_id, cart__user=request.user)
    # If a saved row already exists for this product, merge quantities instead of clashing.
    existing = CartItem.objects.filter(cart=item.cart, product=item.product, saved_for_later=True).first()
    if existing:
        existing.quantity += item.quantity
        existing.save()
        item.delete()
    else:
        item.saved_for_later = True
        item.save()
    return redirect('cart')


@login_required
@require_POST
def move_to_cart(request, item_id):
    item = get_object_or_404(CartItem, id=item_id, cart__user=request.user)
    existing = CartItem.objects.filter(cart=item.cart, product=item.product, saved_for_later=False).first()
    if existing:
        existing.quantity += item.quantity
        existing.save()
        item.delete()
    else:
        item.saved_for_later = False
        item.save()
    return redirect('cart')
