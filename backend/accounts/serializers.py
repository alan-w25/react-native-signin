from rest_framework import serializers
from django.contrib.auth import get_user_model 
from django.contrib.auth.password_validation import validate_password
from django.contrib.auth import authenticate 
from rest_framework.exceptions import AuthenticationFailed



User = get_user_model() 

class UserSerializer(serializers.ModelSerializer): 
    password = serializers.CharField(write_only = True, required=True, validators=[validate_password])
    password2 = serializers.CharField(write_only = True, required=True)
    
    class Meta: 
        model = User 
        fields = ('email', 'username', 'password', 'password2', 'first_name', 'last_name')
        extra_kwargs ={
            'first_name': {'required':False}, 
            'last_name': {'required':False},
        }
        
    def validate(self, attrs): 
        if attrs['password'] != attrs['password2']: 
            raise serializers.ValidationError({'password': 'Password fields did not match'})
        return attrs
    
    def create(self, validated_data): 
        validated_data.pop('password2')
        user = User.objects.create_user(**validated_data)
        return user
    

class LoginSerializer(serializers.Serializer): 
    email = serializers.EmailField() 
    password = serializers.CharField(write_only=True)
    
    def validate(self, data): 
        email = data.get('email')
        password = data.get('password')
        
        if email and password: 
            user = authenticate(request = self.context.get('request'), email=email, password=password)
            if not user:  
                raise AuthenticationFailed('Invalid email or password')
        else: 
            raise serializers.ValidationError('Must include email and password')
        
        data['user'] = user
        return data