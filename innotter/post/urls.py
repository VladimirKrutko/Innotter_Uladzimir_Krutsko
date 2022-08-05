from django.urls import path
from post.views import PostCRUDView, PostCreateView

app_name = 'post'

urlpatterns = [
    path('create/', PostCreateView.as_view()),
    path('postcrud/<int:pk>', PostCRUDView.as_view())
]

