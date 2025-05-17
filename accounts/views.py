from django.shortcuts import render

from .permissions import IsSuperAdmin,IsUserOrSuperAdmin
from .serializers import UserSerializer
from rest_framework.response import Response
from rest_framework.decorators import api_view,permission_classes, authentication_classes
from django.conf import settings
import jwt
from rest_framework import viewsets,permissions

from rest_framework.permissions import AllowAny

from .models import User
from django.contrib.auth.hashers import check_password

from datetime import datetime, timedelta

# Create your views here.



class UsersViewSet(viewsets.ModelViewSet):
    queryset = User.objects.filter(is_superuser=False)
    serializer_class = UserSerializer



    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy', 'list']:
            permission_classes = [IsSuperAdmin]
        elif self.action == 'retrieve':
            permission_classes = [IsUserOrSuperAdmin]
        else:
            permission_classes = [permissions.IsAuthenticated]
        return [permission() for permission in permission_classes]

    def get_queryset(self):
        queryset = self.queryset
     
        return queryset






@api_view(['POST'])
@permission_classes([AllowAny])
@authentication_classes([])
def login(request):
    username = request.data['username']
    password = request.data['password']
    user = User.objects.get(username=username)

    if check_password(password,user.password) :
        payload = {'id': user.id,
                    'username': user.username,
                    'exp': datetime.utcnow() + timedelta(days=1),
                    'iat': datetime.utcnow()
                  }
        token = jwt.encode(payload, settings.SECRET_KEY, algorithm='HS256')

        return Response({
            'token':token,
            })
    else:
        return Response({'Error':'Entered password is wrong !!! '},status=400)
      
