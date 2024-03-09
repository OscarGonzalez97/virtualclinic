from django.urls import path, include

from base.views import UserCreateAPIView, LoginAuthToken

urlpatterns = [
    path('registro/', UserCreateAPIView.as_view(), name='usuario-create'),
    path('login/', LoginAuthToken.as_view(), name='usuario-login'),
]
