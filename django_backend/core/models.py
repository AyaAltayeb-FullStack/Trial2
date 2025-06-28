from django.db import models

# Create your models here.
from django.db import models

class Charger(models.Model):
    charger_id = models.CharField(max_length=100, unique=True)
    model = models.CharField(max_length=100, blank=True)
    vendor = models.CharField(max_length=100, blank=True)
    connected_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.charger_id

class Transaction(models.Model):
    transaction_id = models.IntegerField(unique=True)
    charger = models.ForeignKey(Charger, on_delete=models.CASCADE, related_name="transactions")
    id_tag = models.CharField(max_length=100)
    meter_start = models.IntegerField(null=True, blank=True)
    meter_stop = models.IntegerField(null=True, blank=True)
    started_at = models.DateTimeField()
    stopped_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"Tx {self.transaction_id} @ {self.charger.charger_id}"

class StatusLog(models.Model):
    charger = models.ForeignKey(Charger, on_delete=models.CASCADE, related_name="status_logs")
    event = models.CharField(max_length=100)
    timestamp = models.DateTimeField()
    message = models.TextField(blank=True)

    def __str__(self):
        return f"{self.event} @ {self.timestamp}"
