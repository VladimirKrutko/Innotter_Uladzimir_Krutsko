from django.urls import path
from page.views import (UpdatePageView, AddFollowersPrivatePage, AddFollowersPublicPage,
                        ListPagesView, BlockPageView, ListPagePostView, ListFollowRequestView,
                        SearchPageView)

app_name = 'page'

urlpatterns = [
    path('update_page/<int:pk>/', UpdatePageView.as_view()),
    path('follower_public/<int:pk>/', AddFollowersPublicPage.as_view()),
    path('add-followers-private/<int:pk>/', AddFollowersPrivatePage.as_view()),
    path('list_page/', ListPagesView.as_view()),
    path('block_page/<int:pk>/', BlockPageView.as_view()),
    path('page_post_view/<int:pk>/', ListPagePostView.as_view()),
    path('follow_request/<int:pk>/', ListFollowRequestView.as_view()),
    path('search_page_user/', SearchPageView.as_view())
]
