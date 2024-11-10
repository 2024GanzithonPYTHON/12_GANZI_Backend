# ganzithon/accounts/serializers.py
from dj_rest_auth.registration.serializers import RegisterSerializer
from rest_framework import serializers
from .models import CustomUser

# 유저 정보 상세 시리얼라이저
class CustomUserDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id', 'username', 'password', 'nickname']
        extra_kwargs = {
            'password': {'write_only': True}
        }

# 유저 정보 생성 시리얼라이저
class CustomRegisterSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=150)
    password = serializers.CharField(write_only=True)
    password_confirm = serializers.CharField(write_only=True)
    nickname = serializers.CharField(max_length=100)

    def validate(self, data):
        # 비밀번호 확인
        if data['password'] != data['password_confirm']:
            raise serializers.ValidationError({"password_confirm": ["Passwords do not match."]})

        # username 중복 확인
        if CustomUser.objects.filter(username=data['username']).exists():
            raise serializers.ValidationError({"username": ["A user with that username already exists."]})

        # nickname 중복 확인
        if CustomUser.objects.filter(nickname=data['nickname']).exists():
            raise serializers.ValidationError({"nickname": ["This nickname is already taken."]})

        return data

    def create(self, validated_data):
        user = CustomUser(
            username=validated_data['username'],
            nickname=validated_data['nickname']
        )
        user.set_password(validated_data['password'])
        user.save()
        return user