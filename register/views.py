from django.shortcuts import render
from rest_framework.response import Response
from django.contrib.auth import authenticate
from .serializers import *
from .renderers import *
from django.db.models import F
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import generics, permissions
from rest_framework.permissions import IsAuthenticated
from rest_framework import status


def get_tokens(user):
    refresh = RefreshToken.for_user(user)
    return {
        'access': str(refresh.access_token)
    }


class UserRegistration(generics.ListCreateAPIView):
    renderer_classes = [UserRenderer]

    def post(self, request, format=None):
        if CustomUser.objects.filter(email=request.data.get("email")).exists():
            return Response({"unique-constrain-error": "E-mail already exists."}, status=404)
        if CustomUser.objects.filter(number=request.data.get("number")).exists():
            return Response({"unique-constrain-error": "Number already exists."}, status=404)
        serializer = RegistrationSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            user = serializer.save()
            token = get_tokens(user)
            return Response({'msg': 'Registration Successfull', 'token': token.get("access"), 'user': user.name, 'email': user.email, 'id': user.id})
        return Response(serializer.errors)


class UserLogin(generics.ListCreateAPIView):
    serializer_class = LoginSerializer
    renderer_classes = [UserRenderer]

    def post(self, request, format=None):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            email = serializer.data.get('email')
            password = serializer.data.get('password')
            user = authenticate(email=email, password=password)
            if (user != None):
                token = get_tokens(user)
                return Response({'msg': 'Login Successfull', 'token': token.get("access"), 'user': user.name, 'email': user.email, 'id': user.id})
            else:
                return Response({'errors': {'non_field_errors': ['Email or Password is not valid',]}}, status=401)
        return Response(serializer.errors)


class PeopleListView(generics.ListCreateAPIView):
    serializer_class = PeopleSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return people.objects.filter(user=user)


class UserProfile(generics.RetrieveUpdateAPIView):
    serializer_class=ProfileSerializer
    permission_classes = [IsAuthenticated]
    renderer_classes = [UserRenderer]
    lookup_field='id'
    queryset=CustomUser.objects.all()


# To create a new group and get all groups of a particular member
class GroupCreate(generics.ListCreateAPIView):
    serializer_class = GroupSerializer
    permission_classes = [IsAuthenticated]
    renderer_classes = [UserRenderer]

    def perform_create(self, serializer):
        user = self.request.user
        group = serializer.save()
        group.members.add(user)
        group.save()
        return group

    def get_queryset(self):
        user = self.request.user
        return Group.objects.filter(members=user)


# To get all members of a particular group
class GroupMem(generics.RetrieveAPIView):
    queryset = Group.objects.all()
    serializer_class = UserSerializer  # Use your CustomUser serializer
    lookup_field = 'id'  # Assuming this is the primary key of Group model

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        members = instance.members.all()
        members_serializer = self.get_serializer(members, many=True)
        return Response(members_serializer.data)


# To create request to other people
class Request(generics.ListCreateAPIView):
    serializer_class = GroupRequestSerializer
    permission_classes = [IsAuthenticated]
    renderer_classes = [UserRenderer]

    def post(self, request, *args, **kwargs):
        user_email = request.data.get('user')
        group = request.data.get('group')
        accepted = request.data.get('accepted')
        try:
            user = CustomUser.objects.get(email=user_email)
        except CustomUser.DoesNotExist:
            return Response({"detail": "User not found."}, status=404)
        serializer = GroupRequestSerializer(
            data={"user": user.id, "group": group, "accepted": accepted})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=201)

    def get_queryset(self):
        user = self.request.user
        return GroupRequest.objects.filter(user=user)


# To accept or decline the request of group
class GroupMember(generics.RetrieveUpdateDestroyAPIView):
    queryset = GroupRequest.objects.all()
    serializer_class = GroupRequestSerializer
    lookup_field = 'id'

    def perform_update(self, serializer):
        instance = serializer.save()

        if instance.accepted:
            group = instance.group
            user = instance.user
            group.members.add(user)
            group.save()

        instance.delete()

class GoogleAuth(generics.CreateAPIView):
    serializer_class=GoogleAuthSerializer
    renderer_classes=[UserRenderer,]
    def post(self, request, *args, **kwargs):
        data=request.data
        email=data.get('email')
        name=data.get('name')
        # image=data.get('picture')
        try:
            user = CustomUser.objects.get(email=email)
            created=False
        except CustomUser.DoesNotExist:
            user = CustomUser.objects.create(email=email, name=name)
            created=True
        tokens = get_tokens(user)
        response_data = {
                'msg': 'Authentication Successful',
                'token': tokens,
                'user': user.name,
                'email': user.email,
                'id': user.id
            }

        if created:
            return Response(response_data, status=status.HTTP_201_CREATED)
        else:
            return Response(response_data, status=status.HTTP_200_OK)


          