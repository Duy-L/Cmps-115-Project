from django.conf.urls import url
from django.conf import settings
from django.conf.urls.static import static
#from . import views

from .views import (
    ProductListView, 
    UserProductListView,
    ProductDetailSlugView, 
    ProductFeaturedDetailView,
    ProductFeaturedListView,
    ProductCreateView,
    ProductDeleteView,
    product_delete_view,
    product_update_view,
    ProductUpdateView
    )


urlpatterns = [
    url(r'^$', ProductListView.as_view(), name='list'),
    url(r'^user_products/$', UserProductListView.as_view(), name='user_list'),
    url(r'new', ProductCreateView.as_view(), name='product-create'),
    url(r'^(?P<slug>[\w-]+)/$', ProductDetailSlugView.as_view(), name='detail'),
    url(r'^featured/$', ProductFeaturedDetailView.as_view(), name='featured'),
    url(r'(?P<slug>[\w-]+)/delete', product_delete_view, name='product-delete'),
    url(r'(?P<slug>[\w-]+)/edit', ProductUpdateView.as_view(), name='product-edit'),
]

