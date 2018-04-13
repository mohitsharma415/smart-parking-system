from django.http import JsonResponse
from .models import *
from random import random
from io import BytesIO
from base64 import b64encode
from qrcode import make
from django.views.decorators.csrf import csrf_exempt


def getParkingByZip(request):
    if request.method == "GET":
        _zip = request.GET.get('zip')
        parkings = Parking.objects.filter(_zip__exact=_zip)
        return JsonResponse(data=[i.__json__() for i in parkings], safe=False)


def getSlots(request):
    if request.method == "GET":
        pid = request.GET.get('pid')
        slots = Slot.objects.filter(parentParking=pid)
        return JsonResponse(data=[i.__json__() for i in slots], safe=False)


def getSubSlotAvailability(request):
    if request.method == "GET":
        # A sub slot is free only if there exists no valid transactionID
        # for that date
        sid = request.GET.get('sid')
        date = request.GET.get('date')
        # Get all subslots for a sid
        subslots = SubSlot.objects.filter(parentSlot=sid)
        # Fire 8 queries for each subSlot
        return JsonResponse(data=[{"ssid": i.ssid, "availability":
                            not Transaction.objects.filter(bookedForDate=date, subSlot=i).exists()} for i in subslots],
                            safe=False)
        # returns a [False, True] Array
        # if True then the slot is free else it is booked


@csrf_exempt
def insertTransaction(request):
    if request.method == "POST":
        subSlotID = request.POST.get('ssid')
        ss = SubSlot.objects.filter(ssid=subSlotID)[0]
        uid = request.POST.get('uid')
        date = request.POST.get('date')
        vehicle = request.POST.get('vehicle')
        TransactionID = ss.parentSlot.parentParking.pid + str(random())[2:]
        Transaction(
            TransactionID=TransactionID,
            bookedForDate=date,
            vehicle=vehicle,
            belongsTo=AppUser.objects.filter(uid=uid)[0],
            subSlot=ss).save()
        bio = BytesIO()
        qr = make(TransactionID)
        qr.save(bio, type='JPEG')
        b64qr = b64encode(bio.getvalue())
        return JsonResponse(data={'qr': b64qr.decode('utf-8')})


def verifyQR(request):
    if request.method == "GET":
        try:
            at = request.GET.get('at')
            date = request.GET.get('date')
            if at == 'E':
                pid = request.GET.get('pid')
            elif at == 'S':
                ssid = request.GET.get('ssid')
                print(ssid)
            TransactionID = request.GET.get('qr')
            txnObj = Transaction.objects.get(TransactionID=TransactionID)
            if txnObj.bookedForDate != date:
                return JsonResponse(data={'val': False})
            if at == 'E':
                if txnObj.subSlot.parentSlot.parentParking.pid == pid:
                    return JsonResponse(data={'val': True})
            elif at == 'S':
                if txnObj.subSlot.ssid == ssid:
                    return JsonResponse(data={'val': True})
            return JsonResponse(data={'val': False})
        except Exception as e:
            return JsonResponse(data={'val': False, 'e': str(e)})
