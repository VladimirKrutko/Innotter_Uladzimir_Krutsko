from django.urls import path
from post.views import PostAPIView

app_name = 'post'

urlpatterns = [
    path('create/', PostAPIView.as_view()),
    # path('public_follower/', )
    # path('postcrud/<int:pk>', PostCRUDView.as_view())
]

