from  rest_framework import  serializers
from django.core import validators

from  Users.models import Rols

class RoleSerializer(serializers.ModelSerializer):

    class Meta:
        model = Rols
        fields = ['RoleId']

class RegisterUserSerializer(serializers.Serializer):
    first_name = serializers.CharField(allow_null=False)
    last_name = serializers.CharField(allow_null=False)
    email = serializers.EmailField(allow_null=False)
    password =  serializers.CharField(allow_null=False)
    PhoneNumber = serializers.CharField(max_length=14,validators=[
              validators.RegexValidator(
                  r"^(?:0|98|\+98|\+980|0098|098|00980)?(9\d{9})$",
                  ("Enter a valid phone number"),
                  "invalid",
              ),
          ],
          error_messages={
              "invalid": ("Enter a valid phone number"),
          },allow_null=False)
    state = serializers.CharField(allow_null=False)

class ValidateUserserializer(serializers.Serializer):
    key = serializers.CharField(allow_null=False, allow_blank=False)
    otp = serializers.IntegerField(allow_null=False)

class ResendOtpSerializer(serializers.Serializer):
    PhoneNumber = serializers.CharField(max_length=14,validators=[
              validators.RegexValidator(
                  r"^(?:0|98|\+98|\+980|0098|098|00980)?(9\d{9})$",
                  ("Enter a valid phone number"),
                  "invalid",
              ),
          ],
          error_messages={
              "invalid": ("Enter a valid phone number"),
          },allow_null=False)

class LoginSerializer(serializers.Serializer):
    PhoneNumber = serializers.CharField(max_length=14, validators=[
        validators.RegexValidator(
            r"^(?:0|98|\+98|\+980|0098|098|00980)?(9\d{9})$",
            ("Enter a valid phone number"),
            "invalid",
            ),
        ],
        error_messages={
            "invalid": ("Enter a valid phone number"),
        }, allow_null=False)

    password = serializers.CharField(allow_null=False)

class UrlSerializer(serializers.Serializer):
    otp = serializers.IntegerField(allow_null=False)
    token = serializers.CharField(allow_null=False,allow_blank=False)
    password = serializers.CharField(allow_blank=False,allow_null=False)

class LoginUserSerializer(serializers.Serializer):
    PhoneNumber = serializers.CharField(max_length=14, validators=[
        validators.RegexValidator(
            r"^(?:0|98|\+98|\+980|0098|098|00980)?(9\d{9})$",
            ("Enter a valid phone number"),
            "invalid",
                ),
            ],
        error_messages={
            "invalid": ("Enter a valid phone number"),
        }, allow_null=False)

