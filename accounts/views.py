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

    user.delete()
    return Response({"detail": "회원탈퇴가 완료되었습니다."}, status=status.HTTP_200_OK)

# 유저 정보 조회, 생성 및 수정
@api_view(['GET', 'POST', 'PUT'])
@permission_classes([IsAuthenticated])
def user_info(request):
    user = request.user

    if request.method == 'GET':
        # 유저 정보 조회
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
            },
            "birthday": user.birthday,
            "current_status": user.current_status,
            "relationship_with_child": user.relationship_with_child,
            "child_name": user.child_name
        }, status=status.HTTP_200_OK)

    elif request.method == 'POST':
        # 유저 정보 생성
        email = request.data.get('email')
        postal_code = request.data.get('postal_code')
        city = request.data.get('city')
        address1 = request.data.get('address1')
        address2 = request.data.get('address2')  # 선택 사항
        birthday = request.data.get('birthday')
        current_status = request.data.get('current_status')
        relationship_with_child = request.data.get('relationship_with_child')
        child_name = request.data.get('child_name')

        errors = {}
        if not email:
            errors['email'] = ["This field is required."]
        if not postal_code:
            errors['postal_code'] = ["This field is required."]
        if not city:
            errors['city'] = ["This field is required."]
        if not address1:
            errors['address1'] = ["This field is required."]
        if not birthday:
            errors['birthday'] = ["This field is required."]
        if not current_status:
            errors['current_status'] = ["This field is required."]
        if not relationship_with_child:
            errors['relationship_with_child'] = ["This field is required."]
        if not child_name:
            errors['child_name'] = ["This field is required."]

        if errors:
            return Response(errors, status=status.HTTP_400_BAD_REQUEST)

        # 유저 정보 저장
        user.email = email
        user.postal_code = postal_code
        user.city = city
        user.address1 = address1
        user.address2 = address2  # 선택 사항
        user.birthday = birthday
        user.current_status = current_status
        user.relationship_with_child = relationship_with_child
        user.child_name = child_name
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
            },
            "birthday": user.birthday,
            "current_status": user.current_status,
            "relationship_with_child": user.relationship_with_child,
            "child_name": user.child_name
        }, status=status.HTTP_200_OK)

    elif request.method == 'PUT':
        # 유저 정보 수정
        email = request.data.get('email', user.email)
        postal_code = request.data.get('postal_code', user.postal_code)
        city = request.data.get('city', user.city)
        address1 = request.data.get('address1', user.address1)
        address2 = request.data.get('address2', user.address2)  # 선택 사항
        birthday = request.data.get('birthday', user.birthday)
        current_status = request.data.get('current_status', user.current_status)
        relationship_with_child = request.data.get('relationship_with_child', user.relationship_with_child)
        child_name = request.data.get('child_name', user.child_name)

        # 유저 정보 수정
        user.email = email
        user.postal_code = postal_code
        user.city = city
        user.address1 = address1
        user.address2 = address2  # 선택 사항
        user.birthday = birthday
        user.current_status = current_status
        user.relationship_with_child = relationship_with_child
        user.child_name = child_name
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
            },
            "birthday": user.birthday,
            "current_status": user.current_status,
            "relationship_with_child": user.relationship_with_child,
            "child_name": user.child_name
        }, status=status.HTTP_200_OK)
