"""
URL configuration for ecommerce project.
"""
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),

    # Page routes (server-rendered templates)
    path('', include('core_app.urls')),
    path('products/', include('products_app.urls')),
    path('cart/', include('cart_app.urls')),
    path('accounts/', include('accounts_app.urls')),

    # REST API (DRF + JWT)
    path('api/', include('products_app.api_urls')),
    path('api/auth/', include('accounts_app.api_urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
