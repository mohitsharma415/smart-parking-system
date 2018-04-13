from requests import get, post
from json import loads
from time import time
from math import ceil
from datetime import datetime

base_url = "https://smart-parking-rest.herokuapp.com/"


def getByZips():
    _zip = '999999'
    url = base_url + "getParkingByZip/"
    print(loads(get(url, params={'zip': _zip}).text))


def getSlots():
    _id = "TEST_PARKING"

    url = base_url + "getSlots/"
    print(loads(get(url, params={'pid': _id}).text))


def getSubSlots():
    date = '06-04-2018'
    sid = 'TEST_PARKING_01'

    url = base_url + "getSubSlotAvailability/"
    print(loads(get(url, params={'sid': sid, 'date': date}).text))


def insertTransaction():
    date = '07-04-2018'
    ssid = 'TEST_PARKING_01_8'
    uid = "TEST_UID"
    url = base_url + "insertTransaction/"
    print(loads(post(url, data={'ssid': ssid, 'date': date, 'uid': uid}).text))


def getCurrentSubSot(slotID):
    # Get current time and see in which -3- section it falls i.e. ceil(hour/3)
    currentDateTime = datetime.fromtimestamp(time())
    sslot = ceil((currentDateTime.hour / 3) + (currentDateTime.minute) / 60)
    ssid = slotID + "_" + str(sslot)
    return ssid


def getCurrentDate():
    dt = datetime.fromtimestamp(time())
    return dt.fromtimestamp(time()).strftime("%d-%m-%Y")


def isQRValid(at='E'):
    # E for Entry S for SubSlot
    slotID = 'TEST_PARKING_01'
    pid = 'TEST_PARKING'
    qr = 'TEST_PARKING09879007326455302'
    if at == 'E':
        print(get(base_url+'verifyQR/', params={'at': at, 'date': getCurrentDate(),'qr': qr, 'pid': pid}).text)
    elif at == 'S':
        print(loads(get(base_url+'verifyQR/', params={'at': at, 'date': getCurrentDate(),'qr': qr, 'ssid': getCurrentSubSot(slotID)}).text))


# getByZips()
# getSlots()
# getSubSlots()
# insertTransaction()
# isQRValid('S')