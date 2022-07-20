from django.urls import path
from .views import LoginAPIView, RegistrationAPIView, UploadImageAPIView

app_name = 'user'
urlpatterns = [
    path('registration/', RegistrationAPIView.as_view()),
    path('login/', LoginAPIView.as_view()),
    path('upload/', UploadImageAPIView.as_view())
]