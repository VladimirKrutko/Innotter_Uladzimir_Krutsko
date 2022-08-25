from django.urls import path
from page.views import (UpdatePageView, AddFollowersPrivatePage, AddFollowersPublicPage,
                        ListPagesView, BlockPageView, ListPagePostView, ListFollowRequestView,
                        SearchPageView, )
from page.views import PageViewSet

app_name = 'page'

urlpatterns = [
    path('update_page/<int:pk>/', PageViewSet.as_view({'put': 'update_by_user'})),
    path('follower_public/<int:pk>/', PageViewSet.as_view({'put': 'add_follower_public'})),
    path('add-followers-private/<int:pk>/', PageViewSet.as_view({'put': 'add_follower_private'})),
    path('list_page/', PageViewSet.as_view({'get': 'get_all_pages'})),
    path('block_page/<int:pk>/', BlockPageView.as_view()),
    path('page_post_view/<int:pk>/', ListPagePostView.as_view()),
    path('follow_request/<int:pk>/', PageViewSet.as_view({'get': 'get_follow_requests'})),
    path('search_page_user/', PageViewSet.as_view({'get': 'search_object'}))
]
