from django.urls import path
from . import views

urlpatterns = [
    path("", views.helpgrow_page, name="helpgrow"),
    path("create/", views.request_create, name="helpgrow_create"),
    path("<int:request_id>/accept/", views.accept_request, name="helpgrow_accept"),
    path("<int:request_id>/comment/", views.comment_request, name="helpgrow_comment"),
    path("<int:request_id>/bookmark/", views.bookmark_toggle, name="helpgrow_bookmark"),
    path("<int:request_id>/report/", views.report_create, name="helpgrow_report"),
    path("<int:request_id>/delete/", views.request_delete, name="helpgrow_delete"),
    path("<int:request_id>/approve/<int:user_id>/", views.team_approve, name="helpgrow_approve"),
    path("<int:request_id>/chat/", views.chat_post, name="helpgrow_chat"),
]
