from rest_framework.routers import DefaultRouter
from django.urls import path, include
from .views import UserView, TestData

app_name = 'user'

router = DefaultRouter()
router.register(r'', UserView, basename='user')

urlpatterns = [
    path('', include(router.urls)),
    # path('create-user/', UserCreateView.as_view(), name="create-user"),
    path('test/', TestData.as_view())
]