from django.shortcuts import render
from rest_framework import viewsets,permissions
from rest_framework import generics
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response
from django.contrib.auth.models import Group 

from .models import  User,Loan,LoanStatus
from .serializers import UserSerializer,LoanSerializer,LoanStatusSerializer,LoanListSerializer
from .permission import IsAllowedToCreateLoan,IsAdminOrAgent



class UserViewSet(viewsets.ModelViewSet):
  
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def get_permissions(self):
        """
        Instantiates and returns the list of permissions that this view requires.
        """
        if self.action == 'create':
            permission_classes = [permissions.AllowAny]
        else:
            permission_classes = [permissions.IsAdminUser]
        return [permission() for permission in permission_classes]


class LoanView(viewsets.ModelViewSet):
    queryset = Loan.objects.all()
    serializer_class = LoanSerializer
    model = Loan
    def get_permissions(self):
        """
        Instantiates and returns the list of permissions that this view requires.
        """
        if self.action == 'create':
            permission_classes = [IsAllowedToCreateLoan]
        else:
            permission_classes = [IsAdminOrAgent]
        return [permission() for permission in permission_classes]

    def list(self,request):
        queryset = Loan.objects.all()
        serializer = LoanSerializer(queryset,many = True)
        return Response(serializer.data)

    def perform_create(self,serializer):
        serializer.save(user = self.request.user)

class LoanStatusView(generics.RetrieveUpdateAPIView):
    queryset =  LoanStatus.objects.all()
    serializer_class = LoanStatusSerializer

    def get_permissions(self):
        """
        Instantiates and returns the list of permissions that this view requires.
        """
        permission_classes = [permissions.IsAdminUser]
        return [permission() for permission in permission_classes]

class LoanListView(generics.ListAPIView):

    def get_queryset(self):
        if Group.objects.filter(user=self.request.user,name__in=["admin","agent"]).exists():
            return LoanStatus.objects.all().select_related('loan')
        else:
            return LoanStatus.objects.filter(loan_user=self.request.user).select_related('loan')
    serializer_class = LoanListSerializer


