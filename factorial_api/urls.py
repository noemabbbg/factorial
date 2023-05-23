from django.urls import path
from factorial import views
from django.contrib import admin
from django.urls import include, path
from calcs import calc
from rest_framework import routers
from rest_framework_simplejwt.views import (
    TokenRefreshView, TokenVerifyView,
)
from factorial.views import RegisterView, LoginView, UserView, LogoutView,  delete_calculation
from factorial.views import MyTokenObtainPairView
urlpatterns = [
   # path('', include(router_comics.urls)),
    path('api-auth/', include('rest_framework.urls', namespace = 'rest_framework')),
    path('register', RegisterView.as_view()),
    # path('login', LoginView.as_view()),
    path('user', UserView.as_view()),
    path('logout', LogoutView.as_view()),
    path('admin/', admin.site.urls),
    path('api/', include('factorial.urls')),
    path('api/login/', MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/token/verify/', TokenVerifyView.as_view(), name='token_verify'),
    path('calculate/', views.calculate, name='calculate'),
    path('calculate-gcd/', views.calculate_gcd, name='calculate_gcd'),
    path('history/', views.HistoryView.as_view(), name='history'),
    path('calculate/<int:id>/', views.delete_calculation, name='delete_calculation'),
    
    ]




#  kafka-topics --bootstrap-server=localhost:9092 --list