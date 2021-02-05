from rest_framework import generics
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.permissions import (
    AllowAny,
    IsAuthenticatedOrReadOnly,
    IsAuthenticated,
)


from api.serializers import UserSerializer
from api.serializers import UserInfoSerializer
from api.serializers import OrgSerializer
from api.serializers import OrgSerializerSecond


from api.models import MyUser
from api.models import UserInfo
from api.models import Org

from api.permissions import IsOwnerOrReadOnly


class CreateAccount(generics.CreateAPIView):

    serializer_class = UserSerializer
    permission_classes = (AllowAny,)


class RetriveAccount(generics.RetrieveAPIView):

    permission_classes = (IsAuthenticated,)
    serializer_class = UserSerializer

    def get_queryset(self):
        return MyUser.objects.filter(pk=self.request.user.id)


class UpdateAccount(generics.UpdateAPIView):

    permission_classes = (IsAuthenticated,)
    serializer_class = UserSerializer

    def update(self, request, *args, **kwargs):
        serializer = self.serializer_class(
            request.user, data=request.data, partial=True
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)


class GetUserInfo(generics.RetrieveAPIView):
    serializer_class = UserInfoSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        return UserInfo.objects.filter(user__id=self.request.user.id)


class UpdateUserInfo(generics.UpdateAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = UserInfoSerializer

    def update(self, request, *args, **kwargs):
        serializer = self.serializer_class(
            request.user, data=request.data, partial=True
        )

        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status=status.HTTP_200_OK)


class CreateOrganization(generics.CreateAPIView):
    serializer_class = OrgSerializer
    permission_classes = (IsAuthenticated,)

    def create(self, request, *args, **kwargs):
        serializer = self.serializer_class(
            data=request.data, context={"request": request}
        )

        if serializer.is_valid(raise_exception=True):

            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UpdateOrganization(generics.UpdateAPIView):
    permission_classes = (
        IsAuthenticated,
        IsOwnerOrReadOnly,
    )
    serializer_class = OrgSerializerSecond

    def update(self, request, *args, **kwargs):
        instance = {"user": request.user, "data": request.data}
        serializer = self.serializer_class(instance, data=request.data, partial=True)

        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class DeleteOrganization(generics.DestroyAPIView):
    permission_classes = (
        IsAuthenticated,
        IsOwnerOrReadOnly,
    )

    serializer_class = OrgSerializer

    def get_queryset(self):
        queryset = Org.objects.filter(id=self.kwargs["pk"])
        return queryset

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance.owner is not request.user:
            return Response({'message':'Invalid Permission'}, status=status.HTTP_400_BAD_REQUEST)

        self.perform_destroy(instance)
        return Response({'message': 'Organization Deleted'}, status=status.HTTP_200_OK)


class RetriveOrganization(generics.RetrieveAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = OrgSerializer


class GetAllOrganization(generics.RetrieveAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = OrgSerializer

    def get(self, request, **kwargs):
        queryset =  Org.objects.all()[:kwargs.get("limit")]
        return Response(queryset, status=status.HTTP_200_OK)


class GetSpecificOrganization(generics.RetrieveAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = OrgSerializer
    
    def get(self, request, **kwargs):
        print(kwargs.get("name"))
        queryset =  Org.objects.filter(name__icontains=kwargs.get("name"))
        return Response(queryset, status=status.HTTP_200_OK)

class JoinOrganization(generics.RetrieveAPIView):