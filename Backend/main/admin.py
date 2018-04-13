from django.contrib import admin
from .models import Parking, Slot, AppUser, Transaction, SubSlot, Vehicle

admin.site.register(Parking)
admin.site.register(AppUser)
admin.site.register(Slot)
admin.site.register(SubSlot)
admin.site.register(Transaction)
admin.site.register(Vehicle)

# Register your models here.
