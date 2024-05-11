from datetime import datetime
from decimal import Decimal

from celery import shared_task
from django.db.models import Sum, Q, Value, F
from django.db.models.functions import Concat
from django.db import transaction
from enum import Enum
from .models import Profile, Job, Contract
from .google_sheets import append_row


class SuccessMessage(Enum):
    PAYMENT_SUCCESSFUL = "Payment successful"
    DEPOSIT_SUCCESSFUL = "Deposit successful"


class FailureMessage(Enum):
    INSUFFICIENT_BALANCE = "Insufficient balance"
    ALREADY_PAID_OR_CONTRACT_NOT_IN_PROGRESS = "Job already paid or contract not in progress"
    INVALID_AMOUNT_VALUE = "Invalid amount value"
    DEPOSIT_LIMIT_EXCEEDS = "Deposit amount exceeds 25% of total jobs to pay"
    LESSER_AMOUNT_THAN_PRICE = "The requested amount to pay is lesser than the job price"


@transaction.atomic
def process_job_payment(user_id, job_id, amount_to_pay):

    job = Job.objects.select_for_update().select_related('contract').get(pk=job_id, contract__client__id=user_id)
    if amount_to_pay < job.price:
        raise ValueError(FailureMessage.LESSER_AMOUNT_THAN_PRICE)
    if job.paid or job.contract.status != Contract.StatusChoices.IN_PROGRESS:
        raise ValueError(FailureMessage.ALREADY_PAID_OR_CONTRACT_NOT_IN_PROGRESS.value)

    client = job.contract.client
    contractor = job.contract.contractor
    if client.balance < amount_to_pay:
        raise ValueError(FailureMessage.INSUFFICIENT_BALANCE.value)

    # Process the payment
    client.balance = F('balance') - amount_to_pay
    contractor.balance = F('balance') + amount_to_pay
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
    append_row.delay([str(datetime.now()), client.username, str(amount_to_pay), "Payment"])

    return SuccessMessage.PAYMENT_SUCCESSFUL.value


@transaction.atomic
def deposit_to_balance(user_id, amount):
    client = Profile.objects.select_for_update().get(pk=user_id)

    if amount <= 0:
        raise ValueError(FailureMessage.INVALID_AMOUNT_VALUE.value)

    unpaid_jobs = Job.objects.filter(contract__client_id=user_id, paid=False)
    total_jobs_to_pay = unpaid_jobs.aggregate(total=Sum('price'))['total'] or 0
    max_deposit_allowed = total_jobs_to_pay * Decimal('0.25')

    if amount > max_deposit_allowed:
        raise ValueError(FailureMessage.DEPOSIT_LIMIT_EXCEEDS.value)

    Profile.objects.filter(pk=user_id).update(balance=F('balance') + amount)

    # Log the transaction
    append_row.delay([str(datetime.now()), client.username, str(amount), 'Deposit'])

    return SuccessMessage.DEPOSIT_SUCCESSFUL.value


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
    return Job.objects.select_related('contract').filter(
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


def validate_dates(start_date_str, end_date_str):
    try:
        start_date = datetime.strptime(start_date_str, '%Y-%m-%d').date()
        end_date = datetime.strptime(end_date_str, '%Y-%m-%d').date()
        if start_date > end_date:
            raise ValueError("The start date must not be later than the end date.")
        return start_date, end_date
    except ValueError as e:
        raise ValueError(f"Date error: {str(e)}")
