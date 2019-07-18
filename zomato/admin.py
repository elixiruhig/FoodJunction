from django.contrib import admin
from django.contrib.auth.models import Group as Group2

# Register your models here.
from django.contrib.auth.admin import UserAdmin

from zomato.forms import RegisterForm
from zomato.models import *


class user_admin(UserAdmin):

    add_form = RegisterForm

    list_display = ('username', 'user_id', 'category', 'staff','admin')
    search_fields = ('username', 'user_id', 'category', 'staff','admin')
    list_filter = ('username', 'user_id', 'category')
    ordering = ('username',)
    filter_horizontal = ()

    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Personal info', {'fields': ('name','email','sector','staff','phone','category')}),
        ('Permissions', {'fields': ('admin',)}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'password1', 'password2')}
         ),
    )

admin.site.register(User, user_admin)

class hotel_admin(admin.ModelAdmin):
    list_display = ('name','vendor','sector')
    search_fields = ('name','vendor','sector')
    list_filter = ('name','vendor','sector')
    ordering = ('name',)

admin.site.register(Hotel, hotel_admin)

class cart_admin(admin.ModelAdmin):
    list_display = ('user', 'transaction_id', 'price', 'duration')
    search_fields = ('user', 'transaction_id', 'price', 'duration')
    list_filter = ('user', 'transaction_id', 'price', 'duration')
    ordering = ('transaction_id',)

admin.site.register(Cart, cart_admin)
admin.site.register(Delivery)
admin.site.register(Dish)
admin.site.register(Transaction)
admin.site.unregister(Group2)