from django.shortcuts import render
from products_app.models import Product


def index(request):
    context = {
        'deals_products': Product.objects.filter(is_featured=True)[:5],
        'home_outdoor_products': Product.objects.filter(category='home_outdoor')[:8],
        'electronics_products': Product.objects.filter(category='electronics')[:8],
        'recommended_products': Product.objects.all().order_by('-created_at')[:10],
    }
    return render(request, 'core_app/home.html', context)
