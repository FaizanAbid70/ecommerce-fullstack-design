from django.contrib.auth import login, logout
from django.shortcuts import redirect, render
from rest_framework import generics, permissions
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.response import Response
from rest_framework.views import APIView

from .forms import LoginForm, SignUpForm
from .serializers import RegisterSerializer, UserSerializer


# ---------------------------------------------------------------------------
# Session-based auth for the storefront templates
# ---------------------------------------------------------------------------
def signup_view(request):
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
    else:
        form = SignUpForm()

    return render(request, 'accounts_app/signup.html', {'form': form})


def login_view(request):
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            login(request, form.get_user())
            next_url = request.POST.get('next') or request.GET.get('next') or 'home'
            return redirect(next_url)
    else:
        form = LoginForm(request)

    return render(request, 'accounts_app/login.html', {'form': form})


def logout_view(request):
    logout(request)
    return redirect('home')


# ---------------------------------------------------------------------------
# JWT API endpoints
# ---------------------------------------------------------------------------
class RegisterAPIView(generics.CreateAPIView):
    """
    POST /api/auth/register/  {username, email, password}
    Creates the user AND returns JWT access/refresh tokens right away.
    """
    permission_classes = [permissions.AllowAny]
    serializer_class = RegisterSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        refresh = RefreshToken.for_user(user)
        return Response({
            'user': UserSerializer(user).data,
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        }, status=201)


class MeAPIView(APIView):
    """GET /api/auth/me/ -> current authenticated user's info."""
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        return Response(UserSerializer(request.user).data)
