from django.urls import path
<<<<<<< HEAD
from .views import LoginAPIView, UserAPIView
=======
from user.views import LoginAPIView, RegistrationAPIView
>>>>>>> _26.07.2022_Working_with_page_model

app_name = 'user'

urlpatterns = [
<<<<<<< HEAD
    path('registration/', UserAPIView.as_view({'post': 'post'})),
    path('login/', LoginAPIView.as_view()),
    path('update/', UserAPIView.as_view({'put': 'put'}))
=======
    path('registration/', RegistrationAPIView.as_view()),
    path('login/', LoginAPIView.as_view())
>>>>>>> _26.07.2022_Working_with_page_model
]
