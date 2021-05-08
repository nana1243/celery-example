from django.contrib import admin

# Register your models here.
from .models import Balances, GetData, TransferAmount

admin.site.register(Balances)
admin.site.register(GetData)
admin.site.register(TransferAmount)
