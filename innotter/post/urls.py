from django.urls import path
from post.views import PostAPIView, PostDeleteView

app_name = 'post'

urlpatterns = [
    path('create_post/', PostAPIView.as_view({'post': 'create'})),
    path('delete_post/<int:pk>/', PostDeleteView.as_view()),
    path('update_post/<int:pk>/', PostAPIView.as_view({'put': 'update'})),
    path('put_like/<int:pk>/', PostAPIView.as_view({'put': 'put_like'}))
    # path('public_follower/', )
    # path('postcrud/<int:pk>', PostCRUDView.as_view())
]

