from django.urls import path
from user.views import LoginAPIView, RegistrationAPIView, UserStatistic, UpdateUserAPIView

app_name = 'user'
urlpatterns = [
    path('registration/', RegistrationAPIView.as_view()),
    path('login/', LoginAPIView.as_view()),
    path('user_statistic/', UserStatistic.as_view()),
    path('update_user/', UpdateUserAPIView.as_view())
]
