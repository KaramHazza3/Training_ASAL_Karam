from datetime import datetime, timedelta

from django.core.management.base import BaseCommand
from ...models import Profile, Contract, Job


class Command(BaseCommand):
    help = 'Seed data for initial database population'

    def handle(self, *args, **kwargs):
        current_datetime = datetime.now()
        current_date = current_datetime.date()
        four_days_ago = (current_date - timedelta(days=4))

        # Create profiles
        client1 = Profile.objects.create_user(username='client1', email='client1@example.com', password='password',
                                              first_name='John', last_name='Doe', profession='Software Developer',
                                              user_type='Client', balance=500.00)

        client2 = Profile.objects.create_user(username='client2', email='client2@example.com', password='password',
                                              first_name='John', last_name='Doe', profession='Software Developer',
                                              user_type='Client', balance=500.00)

        client3 = Profile.objects.create_user(username='client3', email='client3@example.com', password='password',
                                              first_name='John', last_name='Doe', profession='QA Developer',
                                              user_type='Client', balance=500.00)

        client4 = Profile.objects.create_user(username='client4', email='client4@example.com', password='password',
                                              first_name='John', last_name='Doe', profession='FrontEnd Developer',
                                              user_type='Client', balance=30.00)

        contractor1 = Profile.objects.create_user(username='contractor1', email='contractor1@example.com',
                                                  password='password', first_name='Muthana', last_name='Smith',
                                                  profession='Graphic Designer', user_type='Contractor', balance=0.00)

        contractor2 = Profile.objects.create_user(username='contractor2', email='contractor2@example.com',
                                                  password='password', first_name='Azeez', last_name='Will',
                                                  profession='Graphic Designer', user_type='Contractor', balance=0.00)

        contractor3 = Profile.objects.create_user(username='contractor3', email='contractor3@example.com',
                                                  password='password', first_name='Yaseen', last_name='Smith',
                                                  profession='Graphic Designer', user_type='Contractor', balance=0.00)

        # Create contracts

        contract1 = Contract.objects.create(terms='Terms for contract 1', status='in_progress',
                                            client=client1,
                                            contractor=contractor1)
        contract2 = Contract.objects.create(terms='Terms for contract 2', status='in_progress',
                                            client=client2,
                                            contractor=contractor2)
        contract3 = Contract.objects.create(terms='Terms for contract 3', status='in_progress',
                                            client=client3,
                                            contractor=contractor2)
        contract4 = Contract.objects.create(terms='Terms for contract 4', status='in_progress',
                                            client=client4,
                                            contractor=contractor2)

        # Create jobs unpaid jobs
        job1 = Job.objects.create(description='Description for job 1', price=100.00, contract=contract1)
        job2 = Job.objects.create(description='Description for job 2', price=150.00, contract=contract1)
        job3 = Job.objects.create(description='Description for job 3', price=80.00, contract=contract2)
        job4 = Job.objects.create(description='Description for job 4', price=90.00, contract=contract2)
        job5 = Job.objects.create(description='Description for job 5', price=60.00, contract=contract3)

        # Create paid jobs
        job6 = Job.objects.create(description='Description for job 6', paid=True, payment_date=current_date,
                                  price=100.00, contract=contract1)
        job7 = Job.objects.create(description='Description for job 7', paid=True, payment_date=four_days_ago,
                                  price=100.00, contract=contract1)
        job8 = Job.objects.create(description='Description for job 8', paid=True, payment_date=four_days_ago,
                                  price=100.00, contract=contract2)
        ob9 = Job.objects.create(description='Description for job 9', paid=True, payment_date=current_date,
                                 price=100.00, contract=contract4)

        self.stdout.write(self.style.SUCCESS('Seed data created successfully.'))
