from rest_framework import serializers
from .models import CustomUser
from .utils import EMAIL_REGEX
from datetime import date
from rest_framework.validators import UniqueValidator

class UserSerializer(serializers.ModelSerializer):
    email = serializers.RegexField(regex=EMAIL_REGEX, required=True, validators=[UniqueValidator(queryset=CustomUser.objects.all())])
    password = serializers.CharField(required= True)
    first_name = serializers.CharField(required=False)
    is_staff = serializers.BooleanField(default=False)
    is_active = serializers.BooleanField(default=True)
    date_joined = serializers.DateField(default=date.today())

    def create(validated_data):
        return CustomUser.objects.create(**validated_data)


    class Meta:
        model = CustomUser
        fields = "__all__"

class LoginRequestSerializer(serializers.Serializer):
    email = serializers.RegexField(regex=EMAIL_REGEX, required=True)
    password = serializers.CharField(required=True)
