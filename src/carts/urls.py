from django.conf.urls import url

from .views import (
    cart_home,
    cart_update_remove,
    cart_update_add,
    cart_clear

    )


urlpatterns = [
    url(r'^$', cart_home, name='home'),
    url(r'^update_remove/$', cart_update_remove, name='update_remove'),
    url(r'^update_add/$', cart_update_add, name='update_add'),
    url(r'^cart_clear/$', cart_clear, name ='cart_clear')

]
