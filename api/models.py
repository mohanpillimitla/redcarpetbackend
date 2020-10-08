import pytz

from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import ugettext_lazy as _
from django.conf import settings

class User(AbstractUser):
    username = models.CharField(max_length=100,blank=True, null=True)
    email = models.EmailField(_('email address'), unique=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name']

    def __str__(self):
        return "{}".format(self.email)



class Loan(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    TIMEZONES = tuple(zip(pytz.all_timezones, pytz.all_timezones))

    amount = models.IntegerField(blank=False)
    duration = models.DateTimeField()
    emi = models.DecimalField( max_digits=19, decimal_places=10)
    interest_rate = models.DecimalField(max_digits=19, decimal_places=10)
    loan_taken_on = models.DateTimeField(auto_now_add=True)
    timezone = models.CharField(max_length=32, choices=TIMEZONES,default='UTC')
    remaing_amount_to_pay = models.DecimalField(blank=False,max_digits=19, decimal_places=10)
    any_discounts = models.DecimalField(blank=True,null=True,max_digits=19, decimal_places=10)
    
class LoanStatus(models.Model):
    STATUS = (
          ("NW","NEW"),
          ("AD","APPROVED"),
          ("RD","REJECTED"),
    )
    
    status_of_loan = models.CharField(max_length=2, choices=STATUS,default="NW")
    loan = models.ForeignKey(Loan,on_delete=models.CASCADE)