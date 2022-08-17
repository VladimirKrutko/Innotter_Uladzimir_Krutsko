from django.urls import path
from post.views import PostAPIView

app_name = 'post'

urlpatterns = [
    path('create_post/', PostAPIView.as_view({'post': 'create'})),
    # path('public_follower/', )
    # path('postcrud/<int:pk>', PostCRUDView.as_view())
]

