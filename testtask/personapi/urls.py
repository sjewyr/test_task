from django.urls import path

from personapi.views import (
    AddFriend,
    AddMailbox,
    DeleteMailbox,
    GetFriends,
    PersonDetailByID,
    PersonDetailBySurname,
    PersonList,
    RemoveFriend,
)

urlpatterns = [
    path("persons/", PersonList.as_view(), name="person-list"),
    path(
        "persons/surname/<str:surname>/",
        PersonDetailBySurname.as_view(),
        name="person-detail-by-surname",
    ),
    path(
        "persons/id/<int:id>/",
        PersonDetailByID.as_view(),
        name="person-detail-by-id",
    ),
    path(
        "persons/<int:person_id>/mailboxes/add/<str:email>/",
        AddMailbox.as_view(),
        name="add_mailbox",
    ),
    path(
        "persons/<int:person_id>/mailboxes/remove/<int:email_id>/",
        DeleteMailbox.as_view(),
        name="delete_mailbox",
    ),
    path(
        "persons/<int:person_id>/friends/add/<int:friend_id>/",
        AddFriend.as_view(),
        name="add_friend",
    ),
    path(
        "persons/<int:person_id>/friends/remove/<int:friend_id>/",
        RemoveFriend.as_view(),
        name="remove_friend",
    ),
    path(
        "persons/<int:person_id>/friends/",
        GetFriends.as_view(),
        name="get_friends",
    ),
]
