from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.quotes),
    url(r'showUser/(?P<user_id>\d+)$', views.showUser),
    url(r'editUser$', views.editUser),
    url(r'editorUser$', views.editorUser),
    url(r'editUserPass$', views.editUserPass),
    url(r'goback$', views.logout),
    url(r'create_message$', views.create_message),
    url(r'delete_message/(?P<mes_id>\d+)$', views.delete_message),
    url(r'like_message/(?P<mes_id>\d+)$', views.like_message),
]