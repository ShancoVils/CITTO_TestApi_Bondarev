from os import write
from django.utils.functional import empty
from rest_framework import serializers, fields
from rest_framework.response import Response
from .models import CustomUser,GroupPerson

 




# class GroupPersonSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = GroupPerson
#         fields = "__all__"



class CustomUserSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only = True)
    email = serializers.CharField(max_length=120)
    FIO = serializers.CharField()
    Official = serializers.CharField()
    person_group_id = serializers.IntegerField()
    activate_code = serializers.CharField(write_only=True)
    person_group = serializers.StringRelatedField()
    password = serializers.CharField(write_only=True)
    depth = 1


    def create(self, validated_data):
        return CustomUser.objects.create_user(**validated_data)

    def update(self, instance, validated_data):
        instance.email = validated_data.get('email', instance.email)
        instance.FIO = validated_data.get('FIO', instance.FIO)
        instance.Official = validated_data.get('Official', instance.Official)
        instance.person_group_id = validated_data.get('person_group_id', instance.person_group_id)
        instance.save()
        return instance