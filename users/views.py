from django.shortcuts import render,redirect,get_object_or_404
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from .forms import RegisterForm
from django.contrib.auth.decorators import login_required
from .models import Cart,CartItem,Order,OrderItem
from food.models import Item

# Create your views here.
def register(request):
    if request.method=="POST":
        form=RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username=form.cleaned_data.get('username')
            messages.success(request,f'Welcome {username}, your account is created :)')
            return redirect('login')
    else:
        form=RegisterForm()
    return render(request,'users/register.html',{'form':form})

@login_required
def profilepage(request):
    return render(request,'users/profile.html')


def homepage(request):
    return render(request,'users/menu.html')
    
@login_required
def add_to_cart(request,item_id):
    item=get_object_or_404(Item,id=item_id)
    cart,created=Cart.objects.get_or_create(user=request.user)
    cart_item,created=CartItem.objects.get_or_create(cart=cart,item=item)
    if not created:
        cart_item.quantity+=1
    else:
        cart_item.quantity=1
    cart_item.save()
    return redirect('users:view_cart')

@login_required
def view_cart(request):
    cart,created=Cart.objects.get_or_create(user=request.user)
    cart_items=cart.items.all()
    cart_details=[]
    for cart_item in cart_items:
        total_price=cart_item.quantity * cart_item.item.item_price
        cart_details.append({
            'item':cart_item.item,
            'quantity':cart_item.quantity,
            'item_price':cart_item.item.item_price,
            'total_price':total_price
        })
    #print(cart_details)
    return render(request,'users/view_cart.html',{'cart':cart,'cart_details':cart_details})

@login_required
def remove_from_cart(request,item_id):
    cart=get_object_or_404(Cart,user=request.user)
    cart_item=get_object_or_404(CartItem,cart=cart,item_id=item_id)

    if cart_item.quantity>1:
        cart_item.quantity-=1
        cart_item.save()
    else:
        cart_item.delete()
    return redirect('users:view_cart')

@login_required
def process_checkout(request):
    cart=get_object_or_404(Cart,user=request.user)
    cart_items=cart.items.all()
    if not cart_items:
        messages.error(request, 'Your cart is empty. Please add items to the cart before proceeding to checkout.')
        return redirect('users:view_cart')
    cart_details=[]
    total_price=0
    for cart_item in cart_items:
        item_total_price=cart_item.quantity * cart_item.item.item_price
        total_price+=item_total_price
        cart_details.append({
            'item':cart_item.item,
            'quantity':cart_item.quantity,
            'item_price':cart_item.item.item_price,
            'total_price':item_total_price
        })
    
    

    print(cart_details)
    print(total_price)

    order=Order.objects.create(user=request.user, total_price=total_price)
    for detail in cart_details:
        OrderItem.objects.create(order=order, item=detail['item'], quantity=detail['quantity'])


    cart_items.delete()
    cart.delete()
    


    messages.success(request,'Your order has been placed successfully!')

    return redirect('users:order_summary',order_id=order.id)


@login_required
def order_summary(request,order_id):
    order=get_object_or_404(Order, id=order_id, user=request.user)
    order_items=order.items.all()
    for item in order_items:
        item.total_price=item.quantity*item.item.item_price
    return render(request, 'users/order_summary.html',{'order':order, 'order_items':order_items})

@login_required
def user_orders(request):
    orders=Order.objects.filter(user=request.user).order_by('created_at')
    return render(request, 'users/user_orders.html',{'orders':orders})


