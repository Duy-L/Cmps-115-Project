from django.conf.urls import url
from . import views
from . import forms


urlpatterns = [
    url(r'^checkout/$', forms.checkout_info, name='checkout'),
    url(r'^process/$', views.payment_process, name='process'),
    url(r'^done/$', views.payment_done, name='done'),
    url(r'^canceled/$', views.payment_canceled, name='canceled'),
]
