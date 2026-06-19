from django.db import models
from django.core.validators import EmailValidator
from django.utils import timezone
import uuid

class Customer(models.Model):
    """
    Customer model for storing customer information
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField(unique=True, validators=[EmailValidator()])
    phone = models.CharField(max_length=20)
    address = models.TextField()
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100, blank=True)
    postal_code = models.CharField(max_length=20, blank=True)
    country = models.CharField(max_length=100, default='USA')
    company = models.CharField(max_length=200, blank=True)
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)
    preferred_contact = models.CharField(
        max_length=10,
        choices=[('email', 'Email'), ('phone', 'Phone'), ('sms', 'SMS')],
        default='email'
    )

    class Meta:
        db_table = 'customers_customer'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['email']),
            models.Index(fields=['phone']),
            models.Index(fields=['created_at']),
        ]

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"

    @property
    def repair_count(self):
        """Get total number of repairs"""
        from apps.repairs.models import Repair
        return Repair.objects.filter(customer=self).count()

    @property
    def diagnostic_count(self):
        """Get total number of diagnostics"""
        from apps.diagnostics.models import Diagnostic
        return Diagnostic.objects.filter(customer=self).count()

    @property
    def total_spent(self):
        """Calculate total amount spent on repairs"""
        from apps.repairs.models import Repair
        repairs = Repair.objects.filter(customer=self, status='completed')
        return sum(r.actual_cost or 0 for r in repairs)
