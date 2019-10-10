from rest_framework import serializers
from django.contrib.auth.models import User


# user serializer
class UserSerializer(serializers.ModelSerializer):

    password = serializers.CharField(
          write_only=True,
    )

    class Meta:
        model = User
        fields = ('id', 'password', 'username', 'email')

    def create(self, validated_data):
        user = super(UserSerializer, self).create(validated_data)
        if 'password' in validated_data:
            user.set_password(validated_data['password'])
            user.save()
        return user

    def update(self, instance, validated_data):
        instance.username = validated_data.get('username', instance.username)
        instance.password = validated_data.get('password', instance.password)
        instance.email = validated_data.get('email', instance.email)
        instance.save()
        return instance


# admin side serializer
class UserManagementSerializer(serializers.ModelSerializer):

    password = serializers.CharField(
          write_only=True,
    )

    class Meta:
        model = User
        fields = "__all__"