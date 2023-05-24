from rest_framework import viewsets
from rest_framework import status
from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404, redirect
from .permissions import UserPermission
from .models import TodoItem, CustomUser
from .serializers import TodoItemSerializer, UserSerializer, LoginSerializer
from rest_framework import serializers
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.contrib.auth import authenticate
from django.views.decorators.csrf import csrf_exempt
from rest_framework.authtoken.models import Token


class TodoItemViewSet(viewsets.ModelViewSet):
    queryset = TodoItem.objects.all()
    serializer_class = TodoItemSerializer
    permission_classes = [UserPermission]


# class UserViewSet(viewsets.ModelViewSet):
#     queryset = CustomUser.objects.all()
#     serializer_class = UserSerializer
#
#     def perform_create(self, serializer):
#         role = self.request.data.get('role')
#         if role and role not in ['creator', 'completer']:
#             raise serializers.ValidationError("Role must be either 'creator' or 'completer'")
#         serializer.save()


class UserView(APIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'register.html'

    def get(self, request):
        serializer = UserSerializer()
        return Response({'serializer': serializer})

    def post(self, request):
        serializer = UserSerializer(data=request.data)
        role = request.data.get('role')
        if role and role not in ['creator', 'completer']:
            raise serializers.ValidationError("Role must be either 'creator' or 'completer'")
        if serializer.is_valid():
            serializer.save()
            return Response({'serializer': serializer}, template_name='login.html')
        return Response({'error': 'invalid', 'serializer': serializer})


class LoginView(APIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'login.html'

    def get(self, request):
        serializer = LoginSerializer()
        return Response({'serializer': serializer})

    def post(self, request):
        username = request.data.get("username")
        password = request.data.get("password")
        if username is None and password is None:
            return Response({'error': 'Please provide both username & password'},
                            status=status.HTTP_400_BAD_REQUEST)

        user = authenticate(username=username, password=password)

        if not user:
            return Response({'error': 'Invalid credentials'},
                            status=status.HTTP_404_NOT_FOUND)

        token, _ = Token.objects.get_or_create(user=user)
        user = CustomUser.objects.get_by_natural_key(username=username)
        serializer = LoginSerializer()
        if user.role == 'creator':
            return Response({'token': token.key}, status=status.HTTP_200_OK, template_name='tasks_creator.html')
        else:
            return Response({'token': token.key, 'user_id': user.id}, status=status.HTTP_200_OK, template_name='tasks_completer.html')
