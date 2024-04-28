from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.db.models import F
from .models import PurchaseOrder, HistoricalPerformance
from django.db.models import Avg

@receiver(post_save, sender=PurchaseOrder)
def update_performance_metrics_on_save(sender, instance, **kwargs):
    if instance and (instance.status == "completed" or instance.quality_rating):
        update_performance_metrics(instance.vendor)

@receiver(post_delete, sender=PurchaseOrder)
def update_performance_metrics_on_delete(sender, instance, **kwargs):
    update_performance_metrics(instance.vendor)

def update_performance_metrics(vendor):
    # On-Time Delivery Rate
    completed_pos = PurchaseOrder.objects.filter(vendor=vendor, status='completed')
    on_time_delivered_pos = completed_pos.filter(delivery_date__gte=F('order_delivered_date')).count()
    total_completed_pos = completed_pos.count()
    on_time_delivery_rate = (on_time_delivered_pos / total_completed_pos) * 100 if total_completed_pos > 0 else 0
    # Only two integers after decimal
    vendor.on_time_delivery_rate = "{:.2f}".format(on_time_delivery_rate).rstrip('0').rstrip('.')

    # Quality Rating Average
    completed_pos_with_rating = completed_pos.filter(quality_rating__isnull=False)
    quality_rating_avg= completed_pos_with_rating.aggregate(avg_rating=Avg('quality_rating'))['avg_rating'] or 0
    vendor.quality_rating_avg = "{:.2f}".format(quality_rating_avg).rstrip('0').rstrip('.')

    # Fulfillment Rate
    successfully_fulfilled_pos = completed_pos.filter(acknowledgment_date__isnull=False)
    fulfillment_rate = (successfully_fulfilled_pos.count() / total_completed_pos) * 100 if total_completed_pos > 0 else 0
    vendor.fulfillment_rate = "{:.2f}".format(fulfillment_rate).rstrip('0').rstrip('.')

    # Average Response Time
    pos_with_acknowledgment =  PurchaseOrder.objects.filter(vendor=vendor,acknowledgment_date__isnull=False)
    response_times = [(po.acknowledgment_date - po.issue_date).total_seconds() / 3600 for po in pos_with_acknowledgment]
    average_response_time = sum(response_times) / len(response_times) if len(response_times) > 0 else 0
    vendor.average_response_time = "{:.2f}".format(average_response_time).rstrip('0').rstrip('.')

    # if there is no changes in the anaylitics, it doesn't create a new Instance
    _ , _ = HistoricalPerformance.objects.get_or_create(
        vendor=vendor,
        on_time_delivery_rate=vendor.on_time_delivery_rate,
        quality_rating_avg=vendor.quality_rating_avg,
        average_response_time=vendor.average_response_time,
        fulfillment_rate=vendor.fulfillment_rate
    )
    vendor.save()
