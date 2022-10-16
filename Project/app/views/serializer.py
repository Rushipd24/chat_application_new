from rest_framework import serializers
from app.models import *


class UserSerializer(serializers.ModelSerializer):
   
    class Meta:
        model = User
        fields = [
            'user_id',
            'first_name',
            'last_name',
            'email',
            'phone',
            'created_date',
            'modified_date',
            'created_by',
            'modified_by',
            ]
class GroupSerializer(serializers.ModelSerializer):
   
    class Meta:
        model = User
        fields = '__all__'