from django.urls import path
from page.views import (UpdatePageView,
                        AddFollowersPrivatePage,
                        AddFollowersPublicPage,
                        ListPagesView)


app_name = 'page'

urlpatterns = [
    path('update_page/', UpdatePageView.as_view()),
    path('followerpublic/<int:pk>/', AddFollowersPublicPage.as_view()),
    path('add-followers-private/<int:pk>', AddFollowersPrivatePage.as_view()),
    path('list_page/', ListPagesView.as_view())
]
