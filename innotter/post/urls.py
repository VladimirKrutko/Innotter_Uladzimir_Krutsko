from django.urls import path
from post.views import PostCRUDView

app_name = 'post'

urlpatterns = [
    path('postcrud/<int:pk>', PostCRUDView.as_view())
]

