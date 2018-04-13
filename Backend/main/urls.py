from django.urls import path
from .views import *

urlpatterns = [
    path('getParkingByZip/', getParkingByZip),
    path('getSlots/', getSlots),
    path('getSubSlotAvailability/', getSubSlotAvailability),
    path('insertTransaction/', insertTransaction),
    path('verifyQR/', verifyQR)
]
