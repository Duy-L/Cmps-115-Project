from django import forms
from django.shortcuts import get_object_or_404, render
from carts.models import Cart
from django.urls import reverse
from django.http import HttpResponseRedirect
from products.models import Product

class CheckoutForm(forms.Form):
    first_name = forms.CharField(required=True, max_length=100, label='First Name:')
    last_name = forms.CharField(required=True, max_length=100, label='Last Name:')
    email = forms.EmailField(required=True, label='Email:')
    address = forms.CharField(required=True, label='Address')
    postal_code = forms.IntegerField(required=True, label='Postal code:')
    city = forms.CharField(required=True, label='City:')
    state = forms.CharField(required=True, label = 'State/Country:')



def checkout_info(request):
    submitted = False

    cart_obj, new_obj = Cart.objects.new_or_get(request)

    if request.method == 'POST':
        form = CheckoutForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            products = cart_obj.products.all()
            shipping = ' '
            for product in products:
                shipping = cd['email'] + '\r\n'
                shipping = shipping + cd['first_name'] + ' ' + cd['last_name'] + '\r\n'
                shipping = shipping + cd['address'] + '\r\n'
                shipping = shipping + cd['city'] + ', ' + cd['state'] +' '+str(cd['postal_code'])
                product.shipping = shipping
                product.save()

            return HttpResponseRedirect(reverse('payment:process'), {'info': form})

    else:
        form = CheckoutForm()
        if 'submitted' in request.GET:
            submitted = True

    return render(request, 'payment/checkout.html', {'cart': cart_obj, 'form': form, 'submitted': submitted})
