from django.urls import path
from page.views import UpdatePageView, AddFollowersPrivatePage, AddFollowersPublicPage


app_name = 'page'

urlpatterns = [
    path('update_page/', UpdatePageView.as_view()),
    path('add_followers_public/', AddFollowersPublicPage.as_view()),
    path('add_followers_public/', AddFollowersPrivatePage.as_view())
]
