from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver


class AppUser(models.Model):
    uid = models.CharField(max_length=100)
    password = models.CharField(max_length=100)

    def __str__(self):
        return self.uid


class Vehicle(models.Model):
    vid = models.CharField(max_length=100)
    vtype = models.CharField(max_length=100)
    number = models.CharField(max_length=100)
    belongsTo = models.ForeignKey(AppUser, on_delete=models.CASCADE)

    def __str__(self):
        return self.vid


class Parking(models.Model):
    pid = models.CharField(max_length=100, primary_key=True)
    title = models.CharField(max_length=300)
    location = models.CharField(max_length=300)
    address = models.CharField(max_length=500)
    _zip = models.CharField(max_length=10)

    def __str__(self):
        return self.pid

    def __json__(self):
        return {"pid": self.pid, "name": self.title, "location": self.location,
                "address": self.address}


class Slot(models.Model):
    sid = models.CharField(max_length=100, primary_key=True)
    charge = models.CharField(max_length=100)
    parentParking = models.ForeignKey(Parking, on_delete=models.CASCADE)

    def __str__(self):
        return self.sid + self.parentParking.pid

    def __json__(self):
        return {'sid': self.sid, 'charge': self.charge,
                "parentParking": self.parentParking.pid}


class SubSlot(models.Model):
    ssid = models.CharField(max_length=100)
    parentSlot = models.ForeignKey(Slot, on_delete=models.CASCADE)

    def __str__(self):
        return self.ssid


class Transaction(models.Model):
    TransactionID = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    valid = models.BooleanField(default=True)
    bookedForDate = models.CharField(max_length=100)
    vehicle = models.ForeignKey(Vehicle, on_delete=models.CASCADE, null=True)
    belongsTo = models.ForeignKey(AppUser, on_delete=models.CASCADE)
    subSlot = models.ForeignKey(SubSlot, on_delete=models.CASCADE)

    def __str__(self):
        return self.TransactionID


@receiver(post_save, sender=Slot, dispatch_uid="create SubSlots")
def create_subslots(sender, instance, created, **kwargs):
    if created:
        for i in range(1, 9):
            SubSlot(ssid=instance.sid + '_' + str(i), parentSlot=instance).save()
    post_save.disconnect(create_subslots, sender=Slot)
# App User has Bookings, Each Booking has some SubSlots
# Each SubSlot belongs to a slot and each Slot belongs to a Parking
