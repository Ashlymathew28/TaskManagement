from django.shortcuts import render

from .permissions import IsAdminOrSuperAdmin, IsSuperAdmin,IsUserOrSuperAdmin
from .serializers import  TaskSerializer, UserSerializer
from rest_framework.response import Response
from rest_framework.decorators import api_view,permission_classes, authentication_classes
from django.conf import settings
import jwt
from rest_framework import viewsets,permissions
from rest_framework.exceptions import PermissionDenied
from rest_framework import status

from rest_framework.permissions import AllowAny
from rest_framework.decorators import action

from .models import Task, User
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

 
    

class TaskViewSet(viewsets.ModelViewSet):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer

    def get_permissions(self):
        if self.action in ['create', 'destroy']:
            permission_classes = [IsAdminOrSuperAdmin]
        else:
            permission_classes = [permissions.IsAuthenticated]
        return [permission() for permission in permission_classes]


        
    def get_queryset(self):
        queryset = self.queryset
        user = self.request.user
        if user.is_admin:
            queryset = queryset.filter(asigned_to__in=user.members.all().values_list('id',flat=True))
        if user.is_admin==False and user.is_superuser ==False:
            queryset =queryset.filter(asigned_to=user.id)
            
        return queryset

    @action(detail=True, methods=['get'], url_path='report')
    def view_report(self, request, pk=None):
        task = self.get_object()
        user = request.user

        if not (user.is_staff or user.is_superuser):
            raise PermissionDenied("Only admins and superadmins can view reports")

        if task.status != 'Completed':
            return Response({'detail': 'Report is only available for completed tasks.'},
                            status=status.HTTP_400_BAD_REQUEST)

        return Response({
            'task_id': task.id,
            'title': task.title,
            'completion_report': task.completion_report,
            'worked_hours': task.worked_hours,
        })




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
      
def login_page(request):
    return render(request, 'login.html')


def user_page(request):
    return render(request, 'users.html')