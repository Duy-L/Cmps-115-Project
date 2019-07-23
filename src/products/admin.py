from django.contrib import admin
from .models import Product

#access to the products in the /admin page
class ProductAdmin(admin.ModelAdmin):
	list_display = ['__str__', 'slug']
	class Meta:
		model = Product

admin.site.register(Product, ProductAdmin)

