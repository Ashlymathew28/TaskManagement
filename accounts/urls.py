
from rest_framework.routers import DefaultRouter
from .views import login,UsersViewSet
from django.urls import path,include

router = DefaultRouter()

router.register(r'user', UsersViewSet,basename='users')
# router.register(r'task', UsersViewSet,basename='task')



urlpatterns = [
    path('',include(router.urls)),
    path('login/', login,name='login'),
]