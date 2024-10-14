from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView

from bms import views

urlpatterns = [
    path('user_signup/', views.signup, name='user_signup'),
    path('user_login/', views.login, name='user_login'),
    path('sayhello/', views.say_hello, name='sayhello'),
    path('token/refresh/', TokenRefreshView.as_view())
]