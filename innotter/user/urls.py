from django.urls import path
from .views import LoginAPIView, UserAPIView

app_name = 'user'

urlpatterns = [
    path('registration/', UserAPIView.as_view({'post': 'post'})),
    path('login/', LoginAPIView.as_view()),
    path('update/', UserAPIView.as_view({'put': 'put'}))
]
