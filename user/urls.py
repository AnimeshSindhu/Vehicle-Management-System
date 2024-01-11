from django.urls import path
from user.views import UserRegistrationView, UserLoginView, UserListCreateView
from .views import CustomTokenObtainPairView

urlpatterns = [
    path('register/', UserRegistrationView.as_view(), name='register'),
    path('login/', UserLoginView.as_view(), name='login'),
    path('display/', UserListCreateView.as_view(), name='display'),
    path('token/', CustomTokenObtainPairView.as_view(), name='token'),
]
