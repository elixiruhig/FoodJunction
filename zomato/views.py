from random import randint

from django.contrib.auth import logout, login
from django.http import HttpResponse
from django.shortcuts import render, redirect

# Create your views here.
from zomato.forms import RegisterForm, LoginForm, HotelForm, MenuForm
from zomato.models import Hotel, Dish, Transaction, User, Cart, Delivery



def homeview(request):
    if request.user.is_authenticated and request.user.is_vendor:
        hts = Hotel.objects.filter(vendor=request.user)
        if not hts:
            if request.method == 'POST':
                form = HotelForm(request.POST, request.FILES)
                if form.is_valid():
                    hotel = form.save(commit=False)
                    hotel.vendor = request.user
                    hotel.save()
                    return redirect('zomato:homeview')
            form = HotelForm()
            return render(request, 'zomato/hotelform.html', {'form': form})

        received_orders = Cart.objects.filter(hotel = Hotel.objects.get(vendor=request.user),status='placed')
        if received_orders:
            itemlist = []
            for order in received_orders:
                items =[]
                txns = Transaction.objects.filter(user=order.user, item__hotel=Hotel.objects.get(vendor=request.user))
                print(txns.count())
                for txn in txns:
                    items.append(txn.item)
                itemlist.append(items)
            print(itemlist)
            lists = zip(received_orders,itemlist)
            if request.method == 'POST':
                    order_id = request.POST['order-id']
                    o = Cart.objects.get(transaction_id=order_id)
                    o.status = 'accepted' if 'accept' in request.POST else 'rejected'
                    o.save()
                    if o.status == 'accepted':
                        delivery_boy = Delivery.objects.filter(busy=False, available=True).order_by('?').first()
                        o.delivery = delivery_boy.user
                        o.status = 'on its way'
                        delivery_boy.order = o
                        delivery_boy.available = False
                        delivery_boy.busy = True
                        o.save()
                        delivery_boy.save()
                        return redirect('/')
                    return redirect('/')
            return render(request,'zomato/homepage.html',{'lists':lists})
        else:
            return render(request, 'zomato/homepage.html',{'your_hotels':hts})
    elif request.user.is_authenticated and request.user.is_customer:
        hotels = Hotel.objects.all()
        dishes = Dish.objects.all()
        orders = Cart.objects.filter(user = request.user)
        return render(request, 'zomato/homepage.html', {'hotels':hotels,'dishes':dishes,'orders':orders})

    elif request.user.is_authenticated and request.user.is_delivery_agent:
        your_orders = Delivery.objects.filter(user=request.user,order__status__iexact='on its way')
        if request.method == 'POST':
            if 'deliver' in request.POST:
                order = Cart.objects.get(transaction_id=request.POST['order-id'])
                order.status = 'delivered'
                order.save()
                order.delete()
                Transaction.objects.filter(user = order.user, item__hotel=order.hotel).delete()
                return redirect('/')

        return render(request,'zomato/homepage.html',{'your_orders':your_orders})

    else: return render(request,'zomato/homepage.html')


def user_logout(request):
    logout(request)

    return render(request, 'zomato/homepage.html')

def user_login(request):
        form = LoginForm(request.POST or None)
        if form.is_valid():
            user_obj = form.cleaned_data.get('user_obj')
            login(request,user_obj)
            if request.user.category == 'Delivery':
                delivery = Delivery.objects.get_or_create(user = request.user)
                return redirect('zomato:homeview')
            return redirect('zomato:homeview')
        return render(request, 'zomato/login.html', {'form':form})

def register(request):
    if request.method == 'POST' and 'submit' in request.POST:
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()

            return redirect('zomato:homeview')
        else:
            return HttpResponse('{}'.format(form.errors))
    form = RegisterForm()
    return render(request, 'zomato/register.html',{'form':form})


def hotelview(request,hotel_id):
    hotel = Hotel.objects.get(hotel_id=hotel_id)
    if request.POST:
        if 'add-dish' in request.POST:
            form = MenuForm(request.POST or None)
            if form.is_valid():
                menu = form.save(commit=False)
                menu.hotel = hotel
                menu.save()
                return redirect('zomato:homeview')
        elif 'add-to-cart' in request.POST:
            if request.user.is_authenticated:
                dish = Dish.objects.get(dish_id=request.POST['dish'])
                qty = request.POST['quantity']
                txn = Transaction(item=dish, user= request.user,quantity=qty)
                txn.save()
                return redirect('zomato:homeview')
            else:
                return redirect('zomato:homeview')

    dishes = Dish.objects.filter(hotel = hotel)
    form = MenuForm()
    return render(request, 'zomato/hotelview.html',{'dishes':dishes,'hotel':hotel,'form':form})

def cartview(request,user_id):
    if request.method == 'POST':
        if 'remove' in request.POST:
            item_id = request.POST['item']
            Transaction.objects.filter(item=Dish.objects.get(id=item_id),user=request.user).first().delete()
            return redirect('/')


    user = User.objects.get(user_id = user_id)
    txns = Transaction.objects.filter(user = user)
    total = 0
    for txn in txns: total+= (txn.item.price*txn.quantity)
    return render(request, 'zomato/cartview.html',{'txns':txns,'total':total,'user':user})

def checkout(request,user_id):
    user = User.objects.get(user_id= user_id)
    txns = Transaction.objects.filter(user=user)
    total = 0
    for txn in txns: total += (txn.item.price*txn.quantity)
    duration = 20 +  ((user.sector - txns[0].item.hotel.sector)%4)*10
    if request.method == 'POST':
        if 'place-order' in request.POST:
            Cart(user = user, price = total, duration = duration, status='placed',hotel= txns[0].item.hotel).save()
            return redirect('zomato:homeview')


    return render(request, 'zomato/checkout.html',{'total':total, 'duration':duration,'txns':txns,'sector':user.sector})

def orderview(request):
    orders = Cart.objects.filter(user=request.user)
    return render(request, 'zomato/orderview.html',{'orders':orders})

def user_profile(request):
    return render(request, 'zomato/profile.html',{'user':request.user})

def hotels(request):
    hotels = Hotel.objects.all()
    return render(request, 'zomato/hotels.html',{'hotels':hotels})

def dishes(request):
    dishes = Dish.objects.all()
    return render(request, 'zomato/dishes.html',{'dishes':dishes})
