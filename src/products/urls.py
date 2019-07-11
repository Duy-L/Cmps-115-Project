from django.conf.urls import url

from .views import (
    ProductListView, 
    ProductDetailSlugView, 
    ProductCreateView
    )


urlpatterns = [
    url(r'^$', ProductListView.as_view(), name='list'),
    url(r'new', ProductCreateView.as_view(), name='product-create'),
    url(r'^(?P<slug>[\w-]+)/$', ProductDetailSlugView.as_view(), name='detail'),
]


