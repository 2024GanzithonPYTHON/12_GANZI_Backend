# ganzithon/purchase/serializers.py
from rest_framework import serializers
from .models import PurchasePost

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
            'min_participants', 'created_at'
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

    def to_representation(self, instance):
        """Customize how the data is serialized"""
        representation = super().to_representation(instance)
        representation['email_content'] = {
            'subject': instance.email_subject,
            'body': instance.email_body,
            'payment_period': instance.payment_period,
            'bank_name': instance.bank_name,
            'account_number': instance.account_number,
            'contact_info': instance.contact_info
        }
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
