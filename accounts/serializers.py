from django.contrib.auth.hashers import make_password
from rest_framework import serializers
from rest_framework.response import Response

from accounts.models import Doctor, Patient, BaseUser, DoctorCategory


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = BaseUser
        read_only_fields = ('role', 'status'),
        fields = ('id', 'username', 'email', 'password', 'status', 'role')
        extra_kwargs = {
            'password': {'write_only': True}
        }


class UserMiniSerializer(serializers.ModelSerializer):
    class Meta:
        model = BaseUser
        fields = ('id', 'username')


class DoctorCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = DoctorCategory
        read_only_fields = ('is_active',)
        fields = ('id', 'title', 'is_active')


class DoctorSerializer(serializers.ModelSerializer):
    parent_user = UserSerializer(read_only=True)
    category = DoctorCategorySerializer(read_only=True)

    class Meta:
        model = Doctor
        fields = ('id', 'parent_user', 'category')


class DoctorMiniSerializer(serializers.ModelSerializer):
    parent_user = UserMiniSerializer(read_only=True)

    class Meta:
        model = Doctor
        fields = ('id', 'parent_user')


class PatientSerializer(serializers.ModelSerializer):
    parent_user = UserSerializer(read_only=True)

    class Meta:
        model = Patient
        fields = ('id', 'parent_user')


class PatientMiniSerializer(serializers.ModelSerializer):
    parent_user = UserMiniSerializer(read_only=True)

    class Meta:
        model = Patient
        fields = ('id', 'parent_user')


class ChangePasswordSerializer(serializers.ModelSerializer):
    current_password = serializers.CharField(
        write_only=True,
        required=True,
        style={'input_type': 'password'}
    )

    new_password = serializers.CharField(
        write_only=True,
        required=True,
        style={'input_type': 'password'}
    )

    class Meta:
        model = BaseUser
        fields = ('current_password', 'new_password')



