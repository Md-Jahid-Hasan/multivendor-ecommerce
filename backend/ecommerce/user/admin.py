from django.contrib import admin
from .models import User, UserAddress, UserPaymentDetails

admin.site.register(User)
admin.site.register(UserAddress)
admin.site.register(UserPaymentDetails)

