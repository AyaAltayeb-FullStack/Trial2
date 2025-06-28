from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import Charger, Transaction, StatusLog

admin.site.register(Charger)
admin.site.register(Transaction)
admin.site.register(StatusLog)
