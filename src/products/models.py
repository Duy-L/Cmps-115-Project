import random
import os
from django.db import models
from django import forms
from django.conf import settings
from django.db.models.signals import pre_save, post_save
from django.urls import reverse
from django.contrib.auth.models import User
from django.db.models import Q
from django.contrib.auth import get_user_model
from PIL import Image
from django.core.validators import MaxValueValidator, MinValueValidator

User = get_user_model()

from .utils import unique_slug_generator

BRANDS= [
	('other', 'Other'),
    ('nike', 'Nike'),
    ('adidas', 'Adidas'),
    ('converse', 'Converse'),
    ('levis', 'Levis'),
    ]

ARTICLES= [
	('other', 'Other'),
	('Outerwear', 'Outerwear'),
	('tops', 'Tops'),
    ('bottoms', 'Bottoms'),
    ('footwear', 'Footwear'),
    ('accesories', 'Accesories'),
    ]

def get_filename_ext(filepath):
	base_name = os.path.basename(filepath)
	name, ext = os.path.splitext(base_name)
	return name, ext

def upload_image_path(instance, filename):
	new_filename = random.randint(1,234423425)
	name, ext = get_filename_ext(filename)
	final_filename = '{new_filename}{ext}'.format(new_filename=new_filename, ext=ext)
	return "products/{new_filename}/{final_filename}".format(
			new_filename=new_filename, 
			final_filename=final_filename
			)
class ProductForm(forms.Form):
	name = forms.CharField()
	description = forms.CharField()
	price = forms.BooleanField()
	image = forms.ImageField()
	brand = forms.CharField()

#EVERY TIME YOU SAVE YOUR MODEL YOU MUST MAKEMIGRATIONS AND MIGRATE IN TERMINAL
#No underscores in name, names singular eg. Product not Products
class ProductQuerySet(models.query.QuerySet):
	def active(self):
		return self.filter(active=True)

	def featured(self):
		return self.filter(featured=True, active=True)

	def search(self, query):
		lookups = (Q(title__icontains=query) | 
				  Q(description__icontains=query) |
				  Q(price__icontains=query) |
				  Q(tag__title__icontains=query) |
			   	  Q(brand__icontains=query) |
			   	  Q(article__icontains=query)
				  )
		#Q(tag_name__icontains=query)
		return self.filter(lookups).distinct()

class ProductManager(models.Manager):
	def get_queryset(self):
		return ProductQuerySet(self.model, using=self._db)

	def all(self):
	 	return self.get_queryset()

	def active(self):
		return self.get_queryset().active()

	def inactive(self):
		return self.get_queryset().filter(active=False)

	def featured(self): #Product.objects.featured()
		return self.get_queryset().featured()

	def get_by_id(self, id):
		qs = self.get_queryset().filter(id=id)
		if qs.count() == 1:
			return qs.first()
		return None

	def search(self, query):
		return self.get_queryset().active().search(query)

class Product(models.Model): 
	title			= models.CharField(max_length=120)
	slug			= models.SlugField(blank=True, unique=True)
	description		= models.TextField()
	price 			= models.DecimalField(decimal_places=2, max_digits=10, default=0.00, validators=[MinValueValidator(0.01)])
	image			= models.ImageField(upload_to=upload_image_path, blank = False, null = False)
	featured		= models.BooleanField(default=False)
	active			= models.BooleanField(default=True)
	timestamp		= models.DateTimeField(auto_now_add=True)
	author 			= models.ForeignKey('auth.User', null=True, blank=True, related_name = 'seller', on_delete=models.DO_NOTHING)
	brand			= models.CharField(max_length = 100, choices=BRANDS, default = 'other')
	article			= models.CharField(max_length = 100, choices=ARTICLES, default = 'other')
	buyer			= models.ForeignKey(User, null=True, blank=True, related_name = 'buyer',on_delete=models.DO_NOTHING)
	shipping		= models.TextField(null=True, blank=True, default = ' ')



	objects = ProductManager()

	def get_absolute_url(self):
		#return "/products/{slug}/".format(slug=self.slug)
		return reverse("products:detail", kwargs={"slug": self.slug})

	def __str__(self):
		return self.title

	def __unicode__(self):
		return self.title
	
	def sorted_by_date(self):
		return self.Product_set.order_by('timestamp')


def product_pre_save_receiver(sender, instance, *args, **kwargs):
	if not instance.slug:
		instance.slug = unique_slug_generator(instance)

pre_save.connect(product_pre_save_receiver, sender=Product)
