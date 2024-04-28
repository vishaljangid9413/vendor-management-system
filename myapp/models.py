from django.db import models
from django.utils import timezone
from django.core.exceptions import ValidationError

class Vendor(models.Model):
    name = models.CharField(max_length=100)
    contact_details = models.TextField()
    address = models.TextField()
    vendor_code = models.CharField(max_length=50, unique=True, null=True, blank=True)
    on_time_delivery_rate = models.FloatField(default=0)
    quality_rating_avg = models.FloatField(default=0)
    average_response_time = models.FloatField(default=0)
    fulfillment_rate = models.FloatField(default=0)
    
    class Meta:
        verbose_name = ("Vendor")
        verbose_name_plural = ("Vendors")

    def __str__(self):
        return self.name
       
    def clean(self):
        if not self.vendor_code:
            # Generate a unique vendor_code based on vendor name and current timestamp
            self.vendor_code = f"{((self.name).split(' '))[0].lower()}-{timezone.now().strftime('%s')}"

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)   


class PurchaseOrder(models.Model):  
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('completed', 'Completed'),
        ('canceled', 'Canceled'),
    ]

    po_number = models.CharField(max_length=50, unique=True, null=True, blank=True)
    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE, related_name="orders")
    order_date = models.DateTimeField(auto_now_add=True)
    delivery_date = models.DateTimeField()
    order_delivered_date = models.DateTimeField(null=True, blank=True)
    items = models.JSONField()
    quantity = models.IntegerField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    quality_rating = models.FloatField(null=True, blank=True)
    issue_date = models.DateTimeField(auto_now_add=True)
    acknowledgment_date = models.DateTimeField(null=True, blank=True)
        
    class Meta:
        verbose_name = ("PurchaseOrder")
        verbose_name_plural = ("PurchaseOrders")

    def __str__(self):
        return self.po_number
    
    def clean(self):
        if not self.po_number:
            # Generate a unique po_number based on vendor ID and order date
            self.po_number = f"{self.vendor.id}-{timezone.now().strftime('%s')}"

        if self.delivery_date.date() < (self.order_date.date() if self.order_date is not None else (timezone.now()).date()):
            raise ValidationError("Delivery date must be the same day or after the order date.")

        # Update the Order Deliverd Date on completion of order 
        if self.pk is not None and (self.status and self.status == "completed") and self.order_delivered_date is None:
            self.order_delivered_date = timezone.now().strftime('%Y-%m-%d')

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

class HistoricalPerformance(models.Model):
    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE, related_name="performance")
    date = models.DateTimeField(auto_now_add=True)
    on_time_delivery_rate = models.FloatField()
    quality_rating_avg = models.FloatField()
    average_response_time = models.FloatField()
    fulfillment_rate = models.FloatField()

    class Meta:
        verbose_name = ("HistoricalPerformance")
        verbose_name_plural = ("HistoricalPerformances")

    def __str__(self):
        return f"{self.vendor.name}"
