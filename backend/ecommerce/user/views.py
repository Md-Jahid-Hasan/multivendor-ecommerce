from rest_framework.response import Response
from rest_framework.generics import CreateAPIView
from rest_framework.viewsets import ModelViewSet
from .serializers import UserCreateSerializer, PdfSerializer
from django.contrib.auth import get_user_model as User
from rest_framework import status, permissions
from .pdf2data import PDFData


class UserView(ModelViewSet):
    serializer_class = UserCreateSerializer
    queryset = User().objects.all()

    def get_permissions(self):
        if self.action == 'create':
            permission_classes = [permissions.AllowAny]
        else:
            permission_classes = [permissions.IsAuthenticated]
        return [permission() for permission in permission_classes]


class TestData(CreateAPIView):
    serializer_class = PdfSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        instance = self.perform_create(serializer)
        print(instance.file)
        data = PDFData(instance.file)
        response = data.get_data_from_pdf()
        headers = self.get_success_headers(serializer.data)
        return Response({'Message': response}, status=status.HTTP_201_CREATED, headers=headers)

    def perform_create(self, serializer):
        instance = serializer.save()
        return instance

