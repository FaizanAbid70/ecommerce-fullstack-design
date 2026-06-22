from rest_framework import serializers
from .models import Product


class ProductSerializer(serializers.ModelSerializer):
    in_stock = serializers.BooleanField(read_only=True)
    discount_percent = serializers.IntegerField(read_only=True)
    category_display = serializers.CharField(source='get_category_display', read_only=True)

    class Meta:
        model = Product
        fields = [
            'id', 'name', 'price', 'old_price', 'image', 'description',
            'category', 'category_display', 'stock', 'rating',
            'is_featured', 'in_stock', 'discount_percent',
            'created_at', 'updated_at',
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']
