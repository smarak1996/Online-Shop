from django.shortcuts import render, redirect
from .models import OrderItem
from .forms import OrderCreateForm
from cart.cart import Cart
from .tasks import order_created
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def order_create(request):
    cart = Cart(request)
    if request.method == 'POST':
        form = OrderCreateForm(request.POST)
        if form.is_valid():
            order = form.save()
            for item in cart:
                OrderItem.objects.create(order=order, product=item['product'], price=item['price'], quantity=item['quantity']) 
            # clear the cart
            cart.clear()
            # launch asynchronous task
            # order_created.delay(order.id)
            # return render(request, 'orders/order/created.html', {'order': order})
            #set the order in the session
            request.session['order_id'] = order.id 
            # redirect to the payment
            return redirect(reverse('payment:process'))
            
    else:
        form = OrderCreateForm()
    return render(request, 'orders/order/create.html', {'cart': cart, 'form': form})
