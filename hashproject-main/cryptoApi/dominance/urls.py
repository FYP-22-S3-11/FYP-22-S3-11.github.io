from django.urls import path
from .views import CheckFile

urlpatterns = [
    path('api/check-file/', CheckFile.as_view(), name='checkfile'),
]


