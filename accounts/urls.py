
from rest_framework.routers import DefaultRouter
from .views import TaskViewSet, login,UsersViewSet, login_page, user_page
from django.urls import path,include

router = DefaultRouter()

router.register(r'user', UsersViewSet,basename='users')
router.register(r'task', TaskViewSet,basename='task')





urlpatterns = [
    path('',include(router.urls)),
    path('login/', login,name='login'),


# admin panel
    path('login-page/', login_page,name='login-page'),
    path('user-page/', user_page,name='user-page'),


]