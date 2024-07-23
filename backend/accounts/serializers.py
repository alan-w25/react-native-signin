from rest_framework import serializers
from django.contrib.auth import get_user_model 
from django.contrib.auth.password_validation import validate_password 
from django.core.exceptions import ValidationError 

User = get_user_model() 

class UserSerializer(serializers.ModelSerializer): 
    password = serializers.CharField(write_only = True, required=True, validators=[validate_password])
    password2 = serializers.CharField(write_only = True, required=True)
    
    class Meta: 
        model = User 
        fields = ('email', 'username', 'password', 'password2')
        extra_kwargs ={
            'first_name': {'required':False}, 
            'last_name': {'required':False}
        }
        
    def validate(self, attrs): 
        if attrs['password'] != attrs['password2']: 
            raise serializers.ValidationError({'password': 'Password fields did not match'})
        return attrs
    
    def create(self, validated_data): 
        validated_data.pop('password2')
        user = User.objects.create_user(**validated_data)
        return user