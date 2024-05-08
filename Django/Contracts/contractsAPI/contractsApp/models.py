from django.contrib.auth.models import AbstractUser
from django.db import models


class Profile(AbstractUser):
    class ProfessionChoices(models.TextChoices):
        CLIENT = "Client", "Client"
        CONTRACTOR = "Contractor", "Contractor"

    profession = models.CharField(max_length=30)
    balance = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    type = models.CharField(max_length=10, choices=ProfessionChoices)
    email = models.EmailField(unique=True)

    def __str__(self):
        return f"{self.username} ({self.profession})"


class Contract(models.Model):
    class StatusChoices(models.TextChoices):
        NEW = "new", "New"
        IN_PROGRESS = "in_progress", "In Progress"
        TERMINATED = "terminated", "Terminated"

    terms = models.TextField()
    status = models.CharField(max_length=15, choices=StatusChoices, default='new')
    client = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='client_contracts')
    contractor = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='contractor_contracts')


class Job(models.Model):
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    paid = models.BooleanField(default=False)
    payment_date = models.DateField(null=True, blank=True)
    contract = models.ForeignKey(Contract, on_delete=models.CASCADE, related_name='jobs')
