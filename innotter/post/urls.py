from django.urls import path
from post.views import PostCreateView

app_name = 'post'

urlpatterns = [
    path('create/', PostCreateView.as_view()),
    # path('public_follower/', )
    # path('postcrud/<int:pk>', PostCRUDView.as_view())
]

