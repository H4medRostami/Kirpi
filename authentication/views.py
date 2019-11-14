from django.shortcuts import get_object_or_404
from authentication.serializer import UserSerializer, UserManagementSerializer
from rest_framework import viewsets, status
from rest_framework import permissions
from django.contrib.auth.models import User
from rest_framework.response import Response


# User side operation :
class SignUp(viewsets.ViewSet):
    """
    Sign up new users

    Authentication : (AllowAny)
    """
    permission_classes = (permissions.AllowAny,)

    def get_serializer(self):
        return UserSerializer()

    def create(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class MyProfile(viewsets.ReadOnlyModelViewSet):
    """
    Fetch current user Profile information

    Authentication : (IsAuthenticated)
    """
    def get_serializer(self):
        return UserSerializer()

    def list(self, request):
        serializer = UserSerializer(request.user)
        return Response(serializer.data)


class EditMyProfile(viewsets.ViewSet):
    """
    Update current user record

    Authentication : (IsAuthenticated)
    """
    permission_classes = (permissions.IsAuthenticated,)

    def get_serializer(self):
        return UserSerializer()

    def partial_update(self, request, pk=None):

        queryset = User.objects.all()
        user = get_object_or_404(queryset, pk=self.request.user.id)
        serializer = UserSerializer(user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# admin side operation :
class UserManagement(viewsets.ModelViewSet):
    """
    CRUD operations on User model

    Authentication : (IsAdmin, IsAuthenticated)
    """
    permission_classes = (permissions.IsAuthenticated, permissions.IsAdminUser,)
    serializer_class = UserManagementSerializer
    queryset = User.objects.all()


