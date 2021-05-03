from django.shortcuts import render
from core.models import CustomUser

from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from rest_framework.authtoken.models import Token

from .serializers import UserSerializer, LoginRequestSerializer
from django.core.exceptions import ValidationError
from .authentication_backend import CoreBackendAuthentication

class RegisterView(APIView):
    def post(self, request):
        data = request.data
        serializer = UserSerializer(data=data)
        if (serializer.is_valid(raise_exception=False)):
            serializer.create(data)
            return Response(data={"Successfully registered"}, status=status.HTTP_200_OK)
        return Response(data={str(serializer.errors)}, status=status.HTTP_404_NOT_FOUND)

class LoginView(APIView):
    def post(self, request):
        data = request.data
        request_serializer = LoginRequestSerializer(data = data)
        if not request_serializer.is_valid(raise_exception=False):
            return Response(data={"Wrong Request Format"}, status=status.HTTP_403_FORBIDDEN)

        user = CoreBackendAuthentication.authenticate(email = request_serializer.validated_data['email'], password = request_serializer.validated_data['password'])
        if user is None:
            return Response(data={"Wrong credentials"}, status=status.HTTP_404_NOT_FOUND)

        token = Token.objects.get_or_create(user=user)
        return Response(data={
            "Token: {token}".format(token = token)
        }, status=status.HTTP_200_OK)

class RegisterView(APIView):
    def post(self, request):
        data = request.data
        request_serializer = UserSerializer(data=data)

        if not request_serializer.is_valid(raise_exception=False):
            return Response(data=request_serializer.errors, status=status.HTTP_405_METHOD_NOT_ALLOWED)
        user = UserSerializer.create(validated_data = request_serializer.validated_data)
        return Response(
            data= {
                "Successfully created user"
            }, 
            status=status.HTTP_200_OK
        )