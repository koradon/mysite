from django.contrib.contenttypes.models import ContentType
from django.core.exceptions import ValidationError
from django.contrib.auth import get_user_model
from django.db.models import Q

from rest_framework.serializers import \
    ModelSerializer, \
    EmailField, \
    CharField, \
    HyperlinkedIdentityField, \
    SerializerMethodField


User = get_user_model()


class UserCreateSerializer(ModelSerializer):
    email = EmailField(label="Email Address")
    email2 = EmailField(label='Confirm Email')

    class Meta:
        model = User
        fields = [
            'username',
            'password',
            'email',
            'email2',
        ]
        extra_kwargs = \
            {
                "password": {
                    "write_only": True
                }
            }

    # Example of general validation
    # def validate(self, data):
    #     email = data['email']
    #     user_qs = User.objects.filter(email=email)
    #     if user_qs.exists():
    #         raise ValidationError("This umail is already registered")
    #     return data

    def validate_email(self, value):
        data = self.get_initial()
        email2 = data.get('email2')
        email1 = value
        if email1 != email2:
            raise ValidationError("Email must match.")

        user_qs = User.objects.filter(email=email2)
        if user_qs.exists():
            raise ValidationError("This umail is already registered")
        return value

    def validate_email2(self, value):
        data = self.get_initial()
        email1 = data.get('email')
        email2 = value
        if email1 != email2:
            raise ValidationError("Email must match.")
        return value

    def create(self, validated_data):
        username = validated_data['username']
        password = validated_data['password']
        email = validated_data['email']
        user_obj = User(
            username=username,
            email=email
        )
        user_obj.set_password(password)
        user_obj.save()
        return validated_data


class UserLoginSerializer(ModelSerializer):
    token = CharField(allow_blank=True, read_only=True)
    username = CharField(allow_blank=True, required=False)
    email = EmailField(label="Email Address", allow_blank=True, required=False)

    class Meta:
        model = User
        fields = [
            'username',
            'password',
            'email',
            'token',
        ]
        extra_kwargs = \
            {
                "password": {
                    "write_only": True
                }
            }

    # Example of general validation
    def validate(self, data):
        user_obj = None
        email = data.get('email', None)
        username = data.get('username', None)
        password = data.get('password')
        if not email or not username:
            raise ValidationError("Username or email is require to login.")

        user = User.objects.filter(
            Q(email=email) |
            Q(username=username)
        ).distinct()
        user = user.exclude(email__isnull=True).exclude(email__iexact='')

        if user.exists() and user.count() == 1:
            user_obj = user.first()
        else:
            raise ValidationError("This username/email is not valid")

        if user_obj:
            if not user_obj.check_password(password):
                raise ValidationError("Incorrect creditensials. Try again.")

        data["token"] = "SOME RANDOM TOKEN"

        return data
