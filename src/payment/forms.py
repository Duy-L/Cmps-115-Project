from django import forms
from django.shortcuts import get_object_or_404, render
from carts.models import Cart
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect


class CheckoutForm(forms.Form):
    first_name = forms.CharField(required=True, max_length=100, label='First Name:')
    last_name = forms.CharField(required=True, max_length=100, label='Last Name:')
    email = forms.EmailField(required=True, label='Email:')
    address = forms.CharField(required=True, label='Address:')
    postal_code = forms.IntegerField(required=True, label='Postal code:')
    city = forms.CharField(required=True, label='City:')


def checkout_info(request):
    submitted = False

    cart_obj, new_obj = Cart.objects.new_or_get(request)

    if request.method == 'POST':
        form = CheckoutForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data

            return HttpResponseRedirect(reverse('payment:process'), {'info': form})

    else:
        form = CheckoutForm()
        if 'submitted' in request.GET:
            submitted = True

    return render(request, 'payment/checkout.html', {'cart': cart_obj, 'form': form, 'submitted': submitted})
