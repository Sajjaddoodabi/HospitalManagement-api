from rest_framework import serializers

from accounts.models import Doctor, Patient, BaseUser


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


class DoctorSerializer(serializers.ModelSerializer):
    parent_user = UserSerializer(read_only=True)

    class Meta:
        model = Doctor
        fields = ('id', 'parent_user')


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
