from django.shortcuts import render, redirect
from .models import OrderItem
from .forms import OrderCreateForm
from cart.cart import Cart
from .tasks import order_created
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import get_object_or_404
from .models import Order
from django.conf import settings 
from django.http import HttpResponse
from django.template.loader import render_to_string
import os,io
import weasyprint
from django.http import HttpResponse
from django.template.loader import get_template
from django.template import loader
# # import pdfkit
# # import base64
from weasyprint import HTML, CSS
# from django.core.mail import EmailMessage

@csrf_exempt
def order_create(request):
    cart = Cart(request)
    if request.method == 'POST':
        form = OrderCreateForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            if cart.coupon:
                order.coupon = cart.coupon
                order.discount = cart.coupon.discount
            order.save()
            for item in cart:
                OrderItem.objects.create(order=order, product=item['product'], price=item['price'], quantity=item['quantity']) 
            # clear the cart
            cart.clear()
            # launch asynchronous task
            # order_created.delay(order.id)
            # return render(request, 'orders/order/created.html', {'order': order})
            # set the order in the session
            request.session['order_id'] = order.id 
            # redirect to the payment
            return redirect(reverse('payment:process'))
            
    else:
        form = OrderCreateForm()
    return render(request, 'orders/order/create.html', {'cart': cart, 'form': form})

@csrf_exempt
@staff_member_required
def admin_order_detail(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    return render(request, 'orders/order/detail.html', {'order': order})

@csrf_exempt
@staff_member_required
def admin_order_pdf(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    html = render_to_string('orders/order/pdf.html',{'order': order})
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'filename= "order_{}.pdf"'.format(order.id)
    weasyprint.HTML(string=html).write_pdf(response,stylesheets=[CSS(string='body { font-size: 10px }')])
    return response