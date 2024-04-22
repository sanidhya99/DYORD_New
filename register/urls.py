from .views import *

from django.urls import path

urlpatterns = [
    path("register/", UserRegistration.as_view(), name="user_creation"),
    path("login/", UserLogin.as_view(), name="user_auth"),
    path("people/", PeopleListView.as_view(), name="poeple"),
    path("profile/<int:id>/", UserProfile.as_view(), name="user_profile"),
    path("creategroup/", GroupCreate.as_view(), name="group_creation"),
    path("request/", Request.as_view(), name="group_request"),
    path("groupmember/<int:id>/", GroupMember.as_view(), name="group_member_approval"),
    path("groupmem/<int:id>/", GroupMem.as_view(), name="group_member"),
    path("google/" ,GoogleAuth.as_view(),name="GoogleAuthentication")
]
