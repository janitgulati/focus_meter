from django.conf.urls import url
from rest_framework.authtoken import views as rest_views
from . import views as local_views

urlpatterns = [
    url(r'^login/', local_views.LoginAccount.as_view(), name='login'),
    url(r'^logout/', local_views.LoginAccount.as_view(), name='logout'),
    url(r'^auth/', local_views.login_form, name='login_form'),
    url(r'^get_auth_token/$', rest_views.obtain_auth_token, name='get_auth_token'),
    url(r'^register/', local_views.LoginAccount.as_view(), name='register')
]