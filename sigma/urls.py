from django.contrib import admin
from django.urls import path, re_path, include
from django.views.generic.base import TemplateView
from rest_framework import routers
from rest_framework.authtoken import views
from frontend.api import TickList, Logout, ValidToken


router = routers.DefaultRouter()
router.register(r'ticks', TickList, base_name='ticks')


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/token/valid/', ValidToken.as_view()),
    path('api/token/', views.obtain_auth_token),
    path('api/logout/', Logout.as_view()),
    path('api/', include(router.urls)),
    re_path(r'^.*$', TemplateView.as_view(template_name='index.html'), name='index'),
]
