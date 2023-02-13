from rest_framework import serializers

from accounts.models import BaseUser


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = BaseUser
        fields = ('id', 'email', 'password')
        extra_kwargs = {
            'password': {'write_only': True}
        }