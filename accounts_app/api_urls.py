from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from . import views

urlpatterns = [
    path('register/', views.RegisterAPIView.as_view(), name='api_register'),
    path('login/', TokenObtainPairView.as_view(), name='api_token_obtain_pair'),
    path('refresh/', TokenRefreshView.as_view(), name='api_token_refresh'),
    path('me/', views.MeAPIView.as_view(), name='api_me'),
]
