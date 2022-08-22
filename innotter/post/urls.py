from django.urls import path
from post.views import PostAPIView, PostDeleteView

app_name = 'post'

urlpatterns = [
    path('create_post/', PostAPIView.as_view({'post': 'create'})),
    path('delete_post/<int:pk>/', PostDeleteView.as_view())
    # path('public_follower/', )
    # path('postcrud/<int:pk>', PostCRUDView.as_view())
]

