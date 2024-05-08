from datetime import datetime, timedelta
from django.core.management.base import BaseCommand
from faker import Faker
from ...models import Profile, Contract, Job


class Command(BaseCommand):
    help = 'Seed data for initial database population'

    def handle(self, *args, **kwargs):
        fake = Faker()

        # Create profiles
        for _ in range(4):
            Profile.objects.create_user(
                username=fake.user_name(),
                email=fake.email(),
                password='password',
                first_name=fake.first_name(),
                last_name=fake.last_name(),
                profession=fake.job(),
                type='Client',
                balance=fake.random_number(digits=3, fix_len=True)
            )

        for _ in range(3):
            Profile.objects.create_user(
                username=fake.user_name(),
                email=fake.email(),
                password='password',
                first_name=fake.first_name(),
                last_name=fake.last_name(),
                profession=fake.job(),
                type='Contractor',
                balance=0.00
            )

        clients = Profile.objects.filter(type='Client')
        contractors = Profile.objects.filter(type='Contractor')

        # Create contracts
        contracts = []
        for client in clients:
            for contractor in contractors:
                contracts.append(Contract.objects.create(
                    terms=fake.text(),
                    status='in_progress',
                    client=client,
                    contractor=contractor
                ))

        # Create jobs
        jobs = []
        for contract in contracts:
            for _ in range(fake.random_int(min=1, max=5)):
                jobs.append(Job.objects.create(
                    description=fake.text(),
                    price=fake.random_number(digits=3, fix_len=True),
                    contract=contract
                ))

        # Mark some jobs as paid
        for job in jobs[:len(jobs) // 2]:
            job.paid = True
            job.payment_date = fake.date_time_between(start_date='-30d', end_date='now').date()
            job.save()

        self.stdout.write(self.style.SUCCESS('Seed data created successfully.'))
