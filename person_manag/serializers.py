from os import write
from rest_framework import serializers
from .models import CustomUser

 
class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        date_joined = serializers.ReadOnlyField()
        model = CustomUser
        fields =  fields = ('id', 'email', 'FIO','Official',
                            'is_active', 'password', 'activate_code')
        extra_kwargs = {'password': {'write_only': True},'activate_code': {'write_only': True}}
        depth = 1
        

    def create(self, validated_data):
        return CustomUser.objects.create_user(**validated_data)

