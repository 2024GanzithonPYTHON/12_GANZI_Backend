# ganzithon/accounts/views.py
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from django.contrib.auth import get_user_model, authenticate
from .serializers import CustomRegisterSerializer
from rest_framework_simplejwt.tokens import RefreshToken

User = get_user_model()

# 회원가입
class CustomRegisterView(APIView):
    def post(self, request):
        serializer = CustomRegisterSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()

            # 토큰 생성
            refresh = RefreshToken.for_user(user)
            access = refresh.access_token

            return Response({
                "access": str(access),
                "refresh": str(refresh),
                "user": {
                    "id": user.id,
                    "username": user.username,
                    "password": user.password,  
                    "nickname": user.nickname
                }
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# 로그인
class CustomLoginView(APIView):
    def post(self, request, *args, **kwargs):
        username = request.data.get('username')
        password = request.data.get('password')

        errors = {}
        if not username:
            errors['username'] = ["This field is required."]
        if not password:
            errors['password'] = ["This field is required."]

        if errors:
            return Response(errors, status=status.HTTP_400_BAD_REQUEST)

        user = authenticate(request, username=username, password=password)
        if user is None:
            return Response({"error": "Invalid username or password."}, status=status.HTTP_400_BAD_REQUEST)

        refresh = RefreshToken.for_user(user)
        return Response({
            "access": str(refresh.access_token),
            "refresh": str(refresh),
            "user": {
                "id": user.id,
                "username": user.username,
                "password": user.password, 
                "nickname": user.nickname
            }
        }, status=status.HTTP_201_CREATED)

# 로그아웃
class CustomLogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            refresh_token = request.data.get("refresh")
            if refresh_token:
                token = RefreshToken(refresh_token)
                token.blacklist()  
            return Response({"detail": "로그아웃 되었습니다."}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

# 회원탈퇴
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def delete_user(request):
    user = request.user
    password = request.data.get('password')

    # 비밀번호 확인
    if not password:
        return Response({"error": "Password is required."}, status=status.HTTP_400_BAD_REQUEST)
    if not user.check_password(password):
        return Response({"error": "Incorrect password."}, status=status.HTTP_400_BAD_REQUEST)

    # 사용자 삭제
    user.delete()
    return Response({"detail": "회원탈퇴가 완료되었습니다."}, status=status.HTTP_200_OK)

# 유저 정보 생성
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_user_info(request):
    user = request.user

    email = request.data.get('email')
    postal_code = request.data.get('postal_code')
    city = request.data.get('city')
    address1 = request.data.get('address1')
    address2 = request.data.get('address2')  # 선택 사항

    errors = {}
    if not email:
        errors['email'] = ["This field is required."]
    if not postal_code:
        errors['postal_code'] = ["This field is required."]
    if not city:
        errors['city'] = ["This field is required."]
    if not address1:
        errors['address1'] = ["This field is required."]

    if errors:
        return Response(errors, status=status.HTTP_400_BAD_REQUEST)

    # 유저 정보 저장
    user.email = email
    user.postal_code = postal_code
    user.city = city
    user.address1 = address1
    user.address2 = address2  # 선택 사항으로 저장
    user.save()

    return Response({
        "id": user.id,
        "username": user.username,
        "nickname": user.nickname,
        "email": user.email,
        "address": {
            "postal_code": user.postal_code,
            "city": user.city,
            "address1": user.address1,
            "address2": user.address2
        }
    }, status=status.HTTP_200_OK)