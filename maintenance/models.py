from django.db import models
from django.utils import timezone
from vehicles.models import Vehicle

class MaintenanceTask(models.Model):
    TASK_TYPES = [
        ('oil_change', 'Oil Change'),
        ('brake_inspection', 'Brake Inspection'),
        ('tire_replacement', 'Tire Replacement'),
        ('engine_diagnostics', 'Engine Diagnostics'),
        ('general_service', 'General Service'),
        ('other', 'Other'),
    ]
    
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    ]
    
    vehicle = models.ForeignKey(Vehicle, on_delete=models.CASCADE, related_name='maintenance_tasks')
    task_type = models.CharField(max_length=50, choices=TASK_TYPES)
    description = models.TextField()
    date_performed = models.DateField(default=timezone.now)
    technician = models.CharField(max_length=100)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='completed')
    notes = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.task_type} for {self.vehicle.registration_number} on {self.date_performed}"