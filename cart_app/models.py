from django.conf import settings
from django.db import models


class Cart(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='cart')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Cart of {self.user.username}"

    @property
    def active_items(self):
        return self.items.filter(saved_for_later=False)

    @property
    def saved_items(self):
        return self.items.filter(saved_for_later=True)

    @property
    def subtotal(self):
        return sum(item.line_total for item in self.active_items)

    @property
    def shipping(self):
        return 10 if self.active_items.exists() else 0

    @property
    def tax(self):
        return round(float(self.subtotal) * 0.05, 2)

    @property
    def total(self):
        return round(float(self.subtotal) + float(self.shipping) + float(self.tax), 2)

    @property
    def total_quantity(self):
        return sum(item.quantity for item in self.active_items)


class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey('products_app.Product', on_delete=models.CASCADE, related_name='cart_items')
    quantity = models.PositiveIntegerField(default=1)
    saved_for_later = models.BooleanField(default=False)
    added_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('cart', 'product', 'saved_for_later')

    def __str__(self):
        return f"{self.quantity} x {self.product.name}"

    @property
    def line_total(self):
        return self.product.price * self.quantity
