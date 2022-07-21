from django.urls import path
from .views import LoginAPIView, UserAPIView, UploadImageAPIView

app_name = 'user'

urlpatterns = [
    path('registration/', UserAPIView.as_view()),
    path('login/', LoginAPIView.as_view()),
    path('upload/', UploadImageAPIView.as_view()),
    path('update/', UserAPIView.as_view())
]
