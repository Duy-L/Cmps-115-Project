from django.core.urlresolvers import reverse
from django.shortcuts import render
from paypal.standard.forms import PayPalPaymentsForm
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from carts.models import Cart
from products.views import product_delete_view


def payment_process(request):
    order_id = request.session.get('order_id')
    host = request.get_host()

    cart_obj, new_obj = Cart.objects.new_or_get(request)
    products = cart_obj.products.all()
    itemNames = ''
    for product in products:
        if (len(itemNames) != 0):
            itemNames += ', '

        itemNames += product.title

    itemNames += '.'

    paypal_dict = {
        'business': settings.PAYPAL_RECEIVER_EMAIL,
        'amount': cart_obj.total,
        'item_name': itemNames,
        'invoice': str(order_id),
        'notify_url': 'http://{}{}'.format(host, reverse('paypal-ipn')),
        'return_url': 'http://{}{}'.format(host, reverse('payment:done')),
        'cancel_return': 'http://{}{}'.format(host, reverse('payment:canceled')),
    }

    form = PayPalPaymentsForm(initial=paypal_dict)
    context = {'form': form}
    return render(request, 'payment/process.html', context)


@csrf_exempt
def payment_done(request):
    cart_obj, new_obj = Cart.objects.new_or_get(request)
    products = cart_obj.products.all()
    for product in products:
        product_delete_view(request, product.slug)

        request.session['cart_items'] = cart_obj.products.count()

    return render(request, 'payment/done.html')


@csrf_exempt
def payment_canceled(request):
    return render(request, 'payment/canceled.html')
