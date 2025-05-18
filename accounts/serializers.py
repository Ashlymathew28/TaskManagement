from rest_framework import serializers
from .models import Task, User


class UserSerializer(serializers.ModelSerializer):
    assigned_user = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields ='__all__'

    def get_task(self,obj):
        # task = Task
        return UserMiniSerializer(obj.members,many=True)
    

class UserMiniSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields =['id','username']


class TaskSerializer(serializers.ModelSerializer):
    user = serializers.SerializerMethodField()

    class Meta:
        model = Task
        fields ='__all__'
    
    def get_user(self,obj):
        return UserMiniSerializer(obj.assigned_user,many=False)
    
