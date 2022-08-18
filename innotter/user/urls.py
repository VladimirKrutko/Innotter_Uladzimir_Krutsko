from django.urls import path
from user.views import LoginAPIView, RegistrationAPIView, TestCellery

app_name = 'user'
urlpatterns = [
    path('registration/', RegistrationAPIView.as_view()),
    path('login/', LoginAPIView.as_view()),
    path('celery/', TestCellery.as_view())
]
