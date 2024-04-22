from rest_framework import serializers
from .models import *

# Registration Serializer


class RegistrationSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(
        style={'input_type': 'password'}, write_only=True)
    email = serializers.EmailField()
    name = serializers.CharField()
    number = serializers.IntegerField()

    class Meta:
        model = CustomUser
        fields = ('email', 'name', 'number','age','gender','bio','image', 'password', 'password2')
        extra_kwargs = {
            'password': {'write_only': True}
        }
    # function to validate

    def validate(self, attrs):
        password = attrs.get('password')
        password2 = attrs.get('password2')
        if (password != password2):
            raise serializers.ValidationError("Both passwords are different!")
        return attrs
    # function to validate user

    def create(self, validated_data):
        user = CustomUser.objects.create_user(**validated_data)
        return user

# Login Serializer


class LoginSerializer(serializers.ModelSerializer):
    email = serializers.EmailField()

    class Meta:
        model = CustomUser
        fields = ('email', 'password')


class PeopleSerializer(serializers.ModelSerializer):
    email = serializers.EmailField()

    class Meta:
        model = people
        fields = ('user', 'email', 'name')

# User Serializer


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ('email', 'name')
class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ('email', 'name','age','number','image','bio','gender')

# Group Serializer


class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = '__all__'

# Group Request Serializer


class GroupRequestSerializer(serializers.ModelSerializer):
    name = serializers.CharField(source='group.name', read_only=True)

    class Meta:
        model = GroupRequest
        # fields = '__all__'
        fields = ['user', 'group', 'accepted', 'name']


class GoogleAuthSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ('email','name')