# ganzithon/purchase/serializers.py
from rest_framework import serializers
from .models import PurchasePost, PurchaseApplication


# 이메일 내용 시리얼라이저
class EmailContentSerializer(serializers.Serializer):
    subject = serializers.CharField(required=True)
    body = serializers.CharField(required=True)
    payment_period = serializers.DateField(required=True)
    bank_name = serializers.CharField(required=True)
    account_number = serializers.CharField(required=True)
    contact_info = serializers.CharField(required=True)

# 공동 구매 게시글 시리얼라이저

class PurchasePostSerializer(serializers.ModelSerializer):
    email_content = EmailContentSerializer(write_only=True)  
    created_at = serializers.SerializerMethodField()

    class Meta:
        model = PurchasePost
        fields = [
            'id', 'user', 'title', 'image', 'tags', 'body',
            'email_content', 'duration_date', 'duration_time',
            'min_participants', 'created_at',
        ]
        read_only_fields = ['user', 'created_at']
        extra_kwargs = {
            'title': {'required': True},
            'body': {'required': True},
            'duration_date': {'required': True},
            'duration_time': {'required': True},
            'min_participants': {'required': True},
            'image': {'required': False},
            'tags': {'required': False},
        }

    def get_created_at(self, obj):
        return obj.created_at.date().isoformat()

    def get_applications(self, obj):
        # 작성자인 경우 신청 내역 반환
        request = self.context.get('request')
        if request and request.user == obj.user:
            return [
                {
                    'nickname': app.user.nickname,
                    'email': app.user.email,
                    'address': app.address
                }
                for app in obj.applications.all()
            ]
        return []  # 작성자가 아닌 경우 빈 리스트 반환

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        request = self.context.get('request')

        # 작성자 여부 확인
        is_author = request.user == instance.user  # 작성자인지 확인

        # 작성자일 때만 email_content 포함
        if is_author:
            representation['email_content'] = {
                'subject': instance.email_subject,
                'body': instance.email_body,
                'payment_period': instance.payment_period,
                'bank_name': instance.bank_name,
                'account_number': instance.account_number,
                'contact_info': instance.contact_info
            }

        # 작성자일 경우에만 신청 내역을 포함
        applications = self.get_applications(instance)
        if applications:
          representation['applications'] = applications

        return representation

    def create(self, validated_data):
        email_content_data = validated_data.pop('email_content')
        purchase_post = PurchasePost.objects.create(
            user=self.context['request'].user,
            title=validated_data['title'],
            image=validated_data.get('image'),
            tags=validated_data.get('tags'),
            body=validated_data['body'],
            email_subject=email_content_data['subject'],
            email_body=email_content_data['body'],
            payment_period=email_content_data['payment_period'],
            bank_name=email_content_data['bank_name'],
            account_number=email_content_data['account_number'],
            contact_info=email_content_data['contact_info'],
            duration_date=validated_data['duration_date'],
            duration_time=validated_data['duration_time'],
            min_participants=validated_data['min_participants']
        )
        return purchase_post

class PurchaseApplicationSerializer(serializers.ModelSerializer):
    post_title = serializers.CharField(source='post.title', read_only=True)  # 게시글 제목
    user_nickname = serializers.CharField(source='user.nickname', read_only=True)  # 신청자 닉네임
    user_email = serializers.EmailField(source='user.email', read_only=True)  # 신청자 이메일
    duration_date = serializers.DateField(source='post.duration_date', read_only=True)  # 게시글 종료 날짜
    tags = serializers.JSONField(source='post.tags', read_only=True)

    class Meta:
        model = PurchaseApplication
        fields = ['id', 'post', 'post_title', 'user', 'user_nickname', 'user_email', 'address', 'duration_date', 'tags']
        read_only_fields = ['post_title', 'user_nickname', 'user_email', 'address', 'duration_date', 'tags']

