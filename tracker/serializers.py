from django.contrib.auth.models import User
from rest_framework import serializers
from .models import ExpenseIncome
from django.contrib.auth.password_validation import validate_password

class UserRegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ('username', 'password', 'password2', 'email', 'first_name', 'last_name')

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password": "Password fields didn't match."})
        return attrs

    def create(self, validated_data):
        validated_data.pop('password2')
        user = User.objects.create_user(**validated_data)
        return user

class ExpenseIncomeSerializer(serializers.ModelSerializer):
    total = serializers.SerializerMethodField()
    class Meta:
        model = ExpenseIncome
        fields = ['id', 'title', 'description', 'amount', 'transaction_type', 'tax', 'tax_type', 'total', 'created_at', 'updated_at']
        read_only_fields = ['id', 'total', 'created_at', 'updated_at']

    def get_total(self, obj):
        return obj.total
