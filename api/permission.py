from rest_framework.permissions import BasePermission

# importing group class from django 
from django.contrib.auth.models import Group

# Custom permission for users with "is_active" = True.
class IsAllowedToCreateLoan(BasePermission):
    """
    Allows access only to "is_active" users.
    """
    def has_permission(self, request, view):
        
        return Group.objects.filter(user=request.user,name="customer").exists()
        
class IsAdminOrAgent(BasePermission):
    def has_permission(self,request,view):
        return Group.objects.filter(user=request.user,name__in=["agent",'admin']).exists()
        