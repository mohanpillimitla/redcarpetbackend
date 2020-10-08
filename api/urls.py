from django.conf.urls import url, include
from django.urls import path
from rest_framework import routers

from .views import UserViewSet,LoanView,LoanStatusView,LoanListView
router = routers.DefaultRouter()
router.register(r'users',UserViewSet,basename='users')
router.register(r'l',LoanView,basename='l')
urlpatterns = [
url(r'^',include(router.urls)),
url(r'^auth/', include('rest_auth.urls')),
path('loanstatus/<int:pk>/',LoanStatusView.as_view()),
path('loanlist/',LoanListView.as_view())
]