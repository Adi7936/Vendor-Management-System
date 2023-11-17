from django.db import models
# from django.contrib.postgres.fields import JSONField
from django.db.models import Avg, Count
from django.db.models.functions import Coalesce
from django.dispatch import receiver
from django.db.models.signals import post_save

# Create your models here.

#Vendors Model
class Vendor(models.Model):
    name = models.CharField(max_length=255)
    contact_details = models.TextField()
    address = models.TextField()
    vendor_code = models.CharField(max_length=50, unique=True)
    on_time_delivery_rate = models.FloatField(default=0.0)
    quality_rating_avg = models.FloatField(default=0.0)
    average_response_time = models.FloatField(default=0.0)
    fulfillment_rate = models.FloatField(default=0.0)


    # def update_performance_metrics(self):
    #     completed_orders = self.purchaseorder_set.filter(status='completed')
    #     total_orders = self.purchaseorder_set.all()

    #     # On-Time Delivery Rate
    #     on_time_delivery_count = completed_orders.filter(delivery_date__lte=models.F('acknowledgment_date')).count()
    #     self.on_time_delivery_rate = (on_time_delivery_count / total_orders.count()) * 100 if total_orders.count() > 0 else 0

    #     # Quality Rating Average
    #     self.quality_rating_avg = completed_orders.aggregate(average_quality=Coalesce(Avg('quality_rating'), 0))['average_quality']

    #     # Average Response Time
    #     response_times = completed_orders.annotate(response_time=models.F('acknowledgment_date') - models.F('issue_date'))
    #     avg_response_time = response_times.aggregate(average_response_time=Coalesce(Avg('response_time'), 0))['average_response_time']
    #     self.average_response_time = avg_response_time.total_seconds() / 60 if avg_response_time else 0

    #     # Fulfillment Rate
    #     self.fulfillment_rate = (completed_orders.filter(status='completed', quality_rating__isnull=False).count() / total_orders.count()) * 100 if total_orders.count() > 0 else 0

    #     self.save()

    def __str__(self):
        return self.name



#purchaseOrder
class PurchaseOrder(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('completed', 'Completed'),
        ('canceled', 'Canceled'),
    ]

    po_number = models.CharField(max_length=255, unique=True)
    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE)
    order_date = models.DateTimeField(auto_now_add=True)
    delivery_date = models.DateTimeField()
    items = models.JSONField()  # Update this line
    quantity = models.IntegerField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    quality_rating = models.FloatField(null=True, blank=True)
    issue_date = models.DateTimeField(auto_now_add=True)
    acknowledgment_date = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"PO {self.po_number} - {self.vendor.name}"
    
    # def save(self, *args, **kwargs):
    #     super().save(*args, **kwargs)
    #     self.vendor.update_performance_metrics()

# # Signal to update vendor performance metrics after creating or updating a purchase order
# @receiver(post_save, sender=PurchaseOrder)
# def update_vendor_performance(sender, instance, created, **kwargs):
#             if created or instance.status == 'completed':
#                 instance.vendor.update_performance_metrics()


class HistoricalPerformance(models.Model):
    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)
    on_time_delivery_rate = models.FloatField(default=0)
    quality_rating_avg = models.FloatField(default=0)
    average_response_time = models.FloatField(default=0)
    fulfillment_rate = models.FloatField(default=0)

    def __str__(self):
        return f"{self.vendor.name} - {self.date}"
    
    
