


from accounts.models import User


# accounts/permissions.py

from rest_framework import permissions

class IsSuperAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.is_superuser

class IsAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.is_admin

class IsUser(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.is_superuser == False and request.user.is_admin == False

class IsAdminOrSuperAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.is_admin or request.user.is_superuser

class IsUserOrSuperAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and (request.user.is_admin == False and request.user.is_superuser==False) or  request.user.is_superuser or request.user.is_superuser
# class AllUser(permissions.BasePermission):
#     def has_permission(self, request, view):
#         return request.user.is_authenticated and (request.user.is_admin == False and request.user.is_superuser==False) or  request.user.is_superuser or request.user.is_superuser
