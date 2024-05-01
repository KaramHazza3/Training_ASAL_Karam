from datetime import datetime, date
from decimal import Decimal
from django.db.models import Sum, Q, Value, F
from django.db.models.functions import Concat

from .models import Profile, Job, Contract
from .google_sheets import append_row


def process_job_payment(user_id, job_id):
    job = Job.objects.get(pk=job_id, contract__client_id=user_id)

    if job.paid or job.contract.status != Contract.StatusChoices.IN_PROGRESS:
        raise ValueError("Job already paid or contract not in progress")

    client = job.contract.client
    contractor = job.contract.contractor
    amount_to_pay = job.price

    if client.balance < amount_to_pay:
        raise ValueError("Insufficient balance")

    # Process the payment
    client.balance -= amount_to_pay
    contractor.balance += amount_to_pay
    client.save()
    contractor.save()

    # Mark job as paid
    job.paid = True
    job.payment_date = datetime.now()
    job.save()

    # Update the contract status
    job.contract.status = Contract.StatusChoices.TERMINATED
    job.contract.save()

    # Log the transaction
    transaction_data = [str(datetime.now()), client.username, str(amount_to_pay), "Payment"]
    append_row(transaction_data)

    return "Payment successful"


def deposit_to_balance(user_id, amount):
    client = Profile.objects.get(pk=user_id)

    if amount <= 0:
        raise ValueError("Invalid amount value")

    unpaid_jobs = Job.objects.filter(contract__client_id=user_id, paid=False)
    total_jobs_to_pay = unpaid_jobs.aggregate(total=Sum('price'))['total'] or 0
    max_deposit_allowed = total_jobs_to_pay * Decimal('0.25')

    if amount > max_deposit_allowed:
        raise ValueError("Deposit amount exceeds 25% of total jobs to pay")

    client.balance += amount
    client.save()

    # Log the transaction
    transaction_data = [str(datetime.now()), client.username, str(amount), 'Deposit']
    append_row(transaction_data)

    return "Deposit successful"


def filter_contracts_by_status_and_user(user_id, status):
    if status and status not in Contract.StatusChoices.values:
        raise ValueError("Invalid Status")

    queryset = Contract.objects.filter(
        Q(client_id=user_id) | Q(contractor_id=user_id)
    )

    if status:
        queryset = queryset.filter(status=status)
    else:
        queryset = queryset.exclude(status=Contract.StatusChoices.TERMINATED)

    return queryset


def get_jobs_for_user(user_id, paid=None, status=None):
    query = Q(contract__client_id=user_id) | Q(contract__contractor_id=user_id)

    if paid is not None:
        query &= Q(paid=paid)

    if status:
        query &= Q(contract__status=status)

    return Job.objects.filter(query)


def get_best_profession(start_date, end_date):
    return Job.objects.filter(
        payment_date__range=[start_date, end_date], paid=True
    ).values(profession=F('contract__contractor__profession')).annotate(total_earnings=Sum('price')).order_by(
        '-total_earnings').first()


def get_best_clients(start_date, end_date, limit):
    return Job.objects.filter(
        payment_date__range=[start_date, end_date], paid=True
    ).values(
        'contract__client__id',
        fullName=Concat('contract__client__first_name', Value(' '), 'contract__client__last_name')
    ).annotate(total_paid=Sum('price')).order_by('-total_paid')[:limit]
