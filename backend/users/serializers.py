from django.core.exceptions import ValidationError
from rest_framework import serializers
from .models import User
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.db.models import Q
from django.shortcuts import get_object_or_404
from food.models import Subscribe


class UserSerializer(serializers.ModelSerializer):
    is_subscribed = serializers.SerializerMethodField()

    def get_is_subscribed(self, user):
        return Subscribe.objects.filter(
            Q(user=user) & Q(subscription = self.context['request'].user.id)
        ).exists()

    class Meta:
        model = User
        fields = (
            'username',
            'email',
            'first_name',
            'last_name',
            'is_subscribed',
        )

class PostUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            'username',
            'email',
            'first_name',
            'last_name',
            'password',
        ]

class ChangePasswordSerializer(serializers.Serializer):
    """
    Serializer for password change endpoint.
    """

    current_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)
