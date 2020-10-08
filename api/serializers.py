from rest_framework import serializers
from .models import User,Loan,LoanStatus

class UserSerializer(serializers.ModelSerializer):
   

    class Meta:
        model = User
        fields = ('email', 'first_name', 'last_name', 'password')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        
        password = validated_data.pop('password')
        user = User(**validated_data)
        user.set_password(password)


        user.save()
        
        return user


class LoanSerializer(serializers.ModelSerializer):
    class Meta:
        model = Loan
        fields =  '__all__' #['amount','duration','emi','interest_rate','loan_taken_on','timezone','remaing_amount_to_pay']
    def create(self, validated_data):
        # we need to add bussiness logic here
        # and complete loan 
        loan = Loan.objects.create(**validated_data)

        loan_status =LoanStatus.objects.create(loan=loan,status_of_loan="NW")
        loan_status.save()
        return loan
  
    def update(self,Loan,validated_data):
        if LoanStatus.get(loan=Loan).status_of_loan == "NW":
            Loan.save()
            return Loan
        else:
            raise ValidationError('you can only edit new loans')
            

class LoanStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = LoanStatus
        fields='__all__'

class LoanListSerializer(serializers.ModelSerializer):
    loan = LoanSerializer()
    class Meta:
        model = LoanStatus
        fields=['id','loan','status_of_loan']
