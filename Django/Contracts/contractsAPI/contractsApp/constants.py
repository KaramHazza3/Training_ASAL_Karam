from enum import Enum


class SuccessMessage(Enum):
    PAYMENT_SUCCESSFUL = "Payment successful"
    DEPOSIT_SUCCESSFUL = "Deposit successful"


class FailureMessage(Enum):
    INSUFFICIENT_BALANCE = "Insufficient balance"
    ALREADY_PAID_OR_CONTRACT_NOT_IN_PROGRESS = "Job already paid or contract not in progress"
    INVALID_AMOUNT_VALUE = "Invalid amount value"
    DEPOSIT_LIMIT_EXCEEDS = "Deposit amount exceeds 25% of total jobs to pay"
    LESSER_AMOUNT_THAN_PRICE = "The requested amount to pay is lesser than the job price"
