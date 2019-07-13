from django.contrib.auth import logout, login
from django.http import HttpResponse
from django.shortcuts import render, redirect

# Create your views here.
from zomato.forms import RegisterForm, LoginForm, HotelForm, MenuForm
from zomato.models import Hotel, Dish, Transaction, User


def homeview(request):

    if request.user.is_authenticated and request.user.is_vendor:
        hts = Hotel.objects.filter(vendor=request.user)
        if not hts:
            if request.method == 'POST':
                form = HotelForm(request.POST,request.FILES)
                if form.is_valid():
                    hotel = form.save(commit=False)
                    hotel.vendor = request.user
                    hotel.save()
                    return redirect('zomato:homeview')
            form = HotelForm()
            return render(request, 'zomato/hotelform.html',{'form':form})
        else:
            return render(request, 'zomato/homepage.html',{'your_hotels':hts})
    else:
        hotels = Hotel.objects.all()
        dishes = Dish.objects.all()
        return render(request, 'zomato/homepage.html', {'hotels':hotels,'dishes':dishes})



def user_logout(request):
    logout(request)
    return render(request, 'zomato/homepage.html')

def user_login(request):
        form = LoginForm(request.POST or None)
        if form.is_valid():
            user_obj = form.cleaned_data.get('user_obj')
            login(request,user_obj)
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
                txn = Transaction(item=dish, user= request.user)
                txn.save()
            else:
                return redirect('zomato:homeview')

    dishes = Dish.objects.filter(hotel = hotel)
    form = MenuForm()
    return render(request, 'zomato/hotelview.html',{'dishes':dishes,'hotel':hotel,'form':form})

def cartview(request,user_id):
    user = User.objects.get(user_id = user_id)
    txns = Transaction.objects.filter(user = user)
    return render(request, 'zomato/cartview.html',{'txns':txns})