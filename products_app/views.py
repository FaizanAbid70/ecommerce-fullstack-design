from django.db.models import Q
from django.shortcuts import render, get_object_or_404
from django_filters import rest_framework as df_filters
from rest_framework import viewsets, filters

from .models import Product
from .serializers import ProductSerializer
from .permissions import IsAdminOrReadOnly


# ---------------------------------------------------------------------------
# DRF API - CRUD for products + search/filter, used by /api/products/
# ---------------------------------------------------------------------------
class ProductFilter(df_filters.FilterSet):
    min_price = df_filters.NumberFilter(field_name='price', lookup_expr='gte')
    max_price = df_filters.NumberFilter(field_name='price', lookup_expr='lte')

    class Meta:
        model = Product
        fields = ['category', 'min_price', 'max_price']


class ProductViewSet(viewsets.ModelViewSet):
    """
    Full CRUD for products.
    - list/retrieve: open to everyone
    - create/update/delete: staff/admin only (see IsAdminOrReadOnly)
    - ?search=name-or-category   -> free text search (name, description, category)
    - ?category=clothing         -> exact category filter
    - ?min_price=10&max_price=50 -> price range
    - ?ordering=price / -price / created_at
    """
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [IsAdminOrReadOnly]
    filterset_class = ProductFilter
    filter_backends = [df_filters.DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['name', 'description', 'category']
    ordering_fields = ['price', 'created_at', 'rating']


# ---------------------------------------------------------------------------
# Page views - server-rendered pages, pulling live data straight from the DB
# ---------------------------------------------------------------------------
def _filtered_queryset(request):
    """Shared search/category/price/rating/sort filtering for the list and grid pages."""
    qs = Product.objects.all()

    query = request.GET.get('q', '').strip()
    if query:
        qs = qs.filter(
            Q(name__icontains=query) | Q(description__icontains=query) | Q(category__icontains=query)
        )

    category = request.GET.get('category', '').strip()
    if category:
        qs = qs.filter(category=category)

    min_price = request.GET.get('min_price', '').strip()
    if min_price:
        try:
            qs = qs.filter(price__gte=float(min_price))
        except ValueError:
            pass

    max_price = request.GET.get('max_price', '').strip()
    if max_price:
        try:
            qs = qs.filter(price__lte=float(max_price))
        except ValueError:
            pass

    min_rating = request.GET.get('min_rating', '').strip()
    if min_rating:
        try:
            qs = qs.filter(rating__gte=float(min_rating))
        except ValueError:
            pass

    sort = request.GET.get('sort', '').strip()
    if sort == 'price_asc':
        qs = qs.order_by('price')
    elif sort == 'price_desc':
        qs = qs.order_by('-price')
    elif sort == 'rating':
        qs = qs.order_by('-rating')
    else:
        qs = qs.order_by('-created_at')

    return qs


def product_list(request):
    products = _filtered_queryset(request)
    context = {
        'products': products,
        'query': request.GET.get('q', ''),
        'categories': Product.CATEGORY_CHOICES,
        'selected_category': request.GET.get('category', ''),
        'selected_sort': request.GET.get('sort', ''),
        'min_price': request.GET.get('min_price', ''),
        'max_price': request.GET.get('max_price', ''),
        'min_rating': request.GET.get('min_rating', ''),
    }
    return render(request, 'products_app/product_list.html', context)


def product_grid(request):
    products = _filtered_queryset(request)
    context = {
        'products': products,
        'query': request.GET.get('q', ''),
        'categories': Product.CATEGORY_CHOICES,
        'selected_category': request.GET.get('category', ''),
        'selected_sort': request.GET.get('sort', ''),
        'min_price': request.GET.get('min_price', ''),
        'max_price': request.GET.get('max_price', ''),
        'min_rating': request.GET.get('min_rating', ''),
    }
    return render(request, 'products_app/product_grid.html', context)


def product_detail(request, pk):
    product = get_object_or_404(Product, pk=pk)
    similar_products = Product.objects.filter(category=product.category).exclude(pk=pk)[:4]
    context = {
        'product': product,
        'similar_products': similar_products,
    }
    return render(request, 'products_app/product_detail.html', context)
