from .views import *
from django.urls import include, path

urlpatterns = [    
    path('user/', UserView.as_view(), name='user-detail'),
    path('user/<int:pk>/', UserView.as_view(), name='user-detail'),
    path('registration/', UserRegistration.as_view(), name='registration'),
    path('login/', LoginView.as_view(), name='login'),
    path('forgetPassword/', ForgetPasswordView.as_view(), name='forget_password'),    
    path('logout/', LogoutView.as_view(), name='logout'),
]