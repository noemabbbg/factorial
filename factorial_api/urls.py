from django.urls import path
from factorial import views
from django.contrib import admin
from django.urls import include, path
from rest_framework import routers
from rest_framework_simplejwt.views import (
    TokenRefreshView, TokenVerifyView,
)

from factorial.views import MyTokenObtainPairView
urlpatterns = [
   # path('', include(router_comics.urls)),
    path('api-auth/', include('rest_framework.urls', namespace = 'rest_framework')),
   
    path('admin/', admin.site.urls),
    path('api/', include('factorial.urls')),
    path('api/login/', MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/token/verify/', TokenVerifyView.as_view(), name='token_verify'),
    path('calculate/', views.calculate, name='calculate'),
    path('calculate-gcd/', views.calculate_gcd, name='calculate_gcd'),
    path('history/', views.HistoryViewSet.as_view({'get': 'list'}), name='history'),
    
    ]

