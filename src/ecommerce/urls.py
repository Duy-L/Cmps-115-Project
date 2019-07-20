"""ecommerce URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""

from django.conf import settings
from django.conf.urls.static import static

from django.conf.urls import url, include
from django.contrib import admin
from django.views.generic import TemplateView

from .views import home_page, about_page, contact_page, login_page, register_page, logout_page, profile_page
from products.views import(
    ProductFeaturedListView,
    ProductFeaturedDetailView,
    product_by_price_lowest,
    product_by_price_highest,
    product_by_date_oldest,
    product_by_date_newest,
)
urlpatterns = [
    url(r'^$', home_page, name='home'),
    url(r'^about/$', about_page, name='about'),
    url(r'^contact/$', contact_page, name='contact'),
    url(r'^login/$', login_page, name='login'),
    url(r'^cart/', include("carts.urls", namespace='cart')),
    url(r'^register/$', register_page, name='register'),
    url(r'logout/$', logout_page, name = 'logout'),
    url(r'^bootstrap/$', TemplateView.as_view(template_name='bootstrap/example.html')),
    url(r'^products/', include("products.urls", namespace='products')),
    url(r'^search/', include("search.urls", namespace='search')),
    url(r'^admin/', admin.site.urls),
    url(r'^featured/$', ProductFeaturedListView.as_view(), name='featured'),
    url(r'^accounts/', include('allauth.urls')),
    url(r'^accounts/profile', profile_page, name='profile_page'),
    url(r'^paypal/', include('paypal.standard.ipn.urls')),
    url(r'^payment/', include('payment.urls', namespace='payment')),
    url(r'^lowestprice/$', product_by_price_lowest, name='lowestprice'),
    url(r'^highestprice/$', product_by_price_highest, name='highestprice'),
    url(r'^oldestdate/$', product_by_date_oldest, name='oldestdate'),
    url(r'^newestdate/$', product_by_date_newest, name='newestdate'),
]


if settings.DEBUG:
    urlpatterns = urlpatterns + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns = urlpatterns + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
