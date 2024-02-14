from django.urls import path
from .views import UserRegistrationView, UserLoginView, UserProfileView, VehicleListCreate, VehicleView, UserChangePasswordView, SendPasswordResetEmailView, UserPasswordResetView, RoleBasedView

urlpatterns = [
    path('register/', UserRegistrationView.as_view(), name='register'),
    path('login/', UserLoginView.as_view(), name='login'),
    path('display/', UserProfileView.as_view(), name='display'),
    path('vehiclecreate/', VehicleListCreate.as_view(), name='vehiclecreate'),
    path('vehicleview/', VehicleView.as_view(), name='vehicleview'),
    path('staffview/', RoleBasedView.as_view(), name='staffview'),
    path('staffview/<int:pk>/', RoleBasedView.as_view(), name='staffview'),
    path('changepassword/', UserChangePasswordView.as_view(), name='changepassword'),
    path('send-reset-password-email/', SendPasswordResetEmailView.as_view(), name='send-reset-password-email'),
    path('reset-password/<str:uid>/<str:token>/', UserPasswordResetView.as_view(), name='reset-password'),
]
