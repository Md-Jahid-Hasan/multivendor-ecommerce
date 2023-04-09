from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainSerializer
from django.contrib.auth import get_user_model as User
from .models import UserAddress, FileSerializer


class PdfSerializer(serializers.ModelSerializer):
    class Meta:
        model = FileSerializer
        fields = '__all__'


class UserAddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserAddress
        fields = '__all__'
        extra_kwargs = {
            'pk': {'read_only': True},
            'user_id': {'read_only': True},
        }


class UserCreateSerializer(serializers.ModelSerializer):
    password1 = serializers.CharField(required=True, write_only=True)
    user_address = UserAddressSerializer(many=True)

    class Meta:
        model = User()
        fields = ['pk', 'name', 'email', 'password', 'password1', 'role', 'user_address']
        extra_kwargs = {
            'password': {'write_only': True},
            'pk': {'read_only': True},
            'user_address': {'read_only': True}
        }

    def validate(self, attrs):
        request = self.context.get("request")

        if request.method == "POST":
            if attrs['password1'] != attrs['password']:
                raise serializers.ValidationError({'password': "Password Don't match"})
        else:
            if 'password' in attrs:
                if 'password1' not in attrs:
                    raise serializers.ValidationError({'detail': "Password Don't match"})
                if attrs['password1'] != attrs['password']:
                    raise serializers.ValidationError({'detail': "Password Don't match"})

        return attrs

    def update(self, instance, validated_data):
        password = validated_data.pop('password1', None)
        user_address = validated_data.pop('user_address', [])
        user = super().update(instance, validated_data)

        for address in user_address:
            address_obj = UserAddress.objects.get(pk=address.pk, user_id=user)
            address_obj.update(**address)
        if password:
            user.set_password(password)
            user.save()
        return user

    def create(self, validated_data):
        validated_data.pop('password1')
        user_address = validated_data.pop('user_address', [])

        user = User().objects.create_user(**validated_data)
        for address in user_address:
            UserAddress.objects.create(user_id=user, **address)

        return user
