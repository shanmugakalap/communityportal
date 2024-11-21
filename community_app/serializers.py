from rest_framework import serializers
from django.contrib.auth.hashers import make_password
from .models import LoginModel,UserModel

class LoginSerializer(serializers.ModelSerializer):
    class Meta:
        model = LoginModel
        fields = '__all__'
        extra_kwargs = {'password': {'write_only': True}}
    def create(self, validated_data):
        user = LoginModel(
            username=validated_data['username'],
            password=make_password(validated_data['password'])
        )
        user.save()
        return user
    
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserModel
        fields = '__all__'