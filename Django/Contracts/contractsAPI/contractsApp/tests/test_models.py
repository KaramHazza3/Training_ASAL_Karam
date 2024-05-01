from datetime import datetime, timedelta
from django.test import TestCase
from rest_framework.authtoken.models import Token
from rest_framework.test import APIClient

from ..models import Profile, Contract, Job


class BaseTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        current_datetime = datetime.now()
        cls.current_date = current_datetime.date()
        cls.four_days_ago = (cls.current_date - timedelta(days=4))
        cls.seven_days_ago = (cls.current_date - timedelta(days=7))
        cls.ten_days_ago = (cls.current_date - timedelta(days=10))

        cls.test_client1 = Profile.objects.create_user(username='testclient', email='testclient@mail.com',
                                                       password='password',
                                                       first_name='John', last_name='Doe',
                                                       profession='Software Developer',
                                                       user_type='Client', balance=500.00)

        cls.test_client2 = Profile.objects.create_user(username='client2', email='client2@example.com',
                                                       password='password',
                                                       first_name='Mhmmad', last_name='Doe',
                                                       profession='Software Engineer',
                                                       user_type='Client', balance=500.00)

        cls.test_client3 = Profile.objects.create_user(username='client3', email='client3@example.com',
                                                       password='password',
                                                       first_name='Ahmad', last_name='Doe',
                                                       profession='QA Developer',
                                                       user_type='Client', balance=20.00)

        cls.test_client4 = Profile.objects.create_user(username='client4', email='client4@example.com',
                                                       password='password',
                                                       first_name='Kareem', last_name='Doe',
                                                       profession='FrontEnd Developer',
                                                       user_type='Client', balance=500.00)

        cls.test_contractor1 = Profile.objects.create_user(username='testcontractor', email='contractor1@example.com',
                                                           password='password', first_name='Jane', last_name='Smith',
                                                           profession='Graphic Designer', user_type='Contractor',
                                                           balance=0.00)
        cls.test_contractor2 = Profile.objects.create_user(username='contractor2', email='contractor2@example.com',
                                                           password='password', first_name='Jane', last_name='Smith',
                                                           profession='Graphic Designer', user_type='Contractor',
                                                           balance=0.00)

        cls.contract1 = Contract.objects.create(terms='Terms for contract 1', status='in_progress',
                                                client=cls.test_client1,
                                                contractor=cls.test_contractor1)
        cls.contract2 = Contract.objects.create(terms='Terms for contract 2', status='in_progress',
                                                client=cls.test_client2,
                                                contractor=cls.test_contractor2)
        cls.contract3 = Contract.objects.create(terms='Terms for contract 3', status='in_progress',
                                                client=cls.test_client3,
                                                contractor=cls.test_contractor2)
        cls.contract4 = Contract.objects.create(terms='Terms for contract 4', status='in_progress',
                                                client=cls.test_client4,
                                                contractor=cls.test_contractor2)

        cls.job1 = Job.objects.create(description='Description for job 1', price=100.00, contract=cls.contract1)
        cls.job2 = Job.objects.create(description='Description for job 2', price=150.00, contract=cls.contract1)
        cls.job3 = Job.objects.create(description='Description for job 3', price=80.00, contract=cls.contract2)
        cls.job4 = Job.objects.create(description='Description for job 4', price=90.00, contract=cls.contract2)
        cls.job5 = Job.objects.create(description='Description for job 5', price=60.00, contract=cls.contract3)
        cls.job6 = Job.objects.create(description='Description for job 6', paid=True, payment_date=cls.current_date,
                                      price=100.00, contract=cls.contract1)
        cls.job7 = Job.objects.create(description='Description for job 7', paid=True, payment_date=cls.four_days_ago,
                                      price=100.00, contract=cls.contract1)
        cls.job8 = Job.objects.create(description='Description for job 8', paid=True, payment_date=cls.four_days_ago,
                                      price=100.00, contract=cls.contract2)
        cls.job9 = Job.objects.create(description='Description for job 9', paid=True, payment_date=cls.current_date,
                                      price=100.00, contract=cls.contract4)

    def set_auth_token(self, user):
        self.requester = APIClient()
        token = Token.objects.create(user=user)
        self.requester.credentials(HTTP_AUTHORIZATION='Token ' + token.key)


class ProfileModelTest(BaseTestCase):
    def test_created_client(self):
        profile = Profile.objects.get(username='testclient')
        email_field_label = profile._meta.get_field('email').verbose_name
        self.assertEqual(email_field_label, 'email')
        self.assertEqual(profile.email, 'testclient@mail.com')
        self.assertEqual(profile.user_type, 'Client')
        self.assertEqual(profile.balance, 500.00)

    def test_created_contractor(self):
        profile = Profile.objects.get(username='testcontractor')
        user_type_field_label = profile._meta.get_field('user_type').verbose_name
        self.assertEqual(user_type_field_label, 'user type')
        self.assertEqual(profile.profession, 'Graphic Designer')
        self.assertEqual(profile.user_type, 'Contractor')
        self.assertEqual(profile.balance, 0.00)


class ContractModelTest(BaseTestCase):
    def test_created_contract(self):
        contract = Contract.objects.get(id=1)
        status_field_label = contract._meta.get_field('status').verbose_name
        terms_field_label = contract._meta.get_field('terms').verbose_name
        self.assertEqual(status_field_label, 'status')
        self.assertEqual(terms_field_label, 'terms')
        self.assertEqual(contract.status, 'in_progress')
        self.assertEqual(contract.terms, 'Terms for contract 1')


class JobModelTest(BaseTestCase):
    def test_created_job(self):
        job = Job.objects.get(id=1)
        description_field_label = job._meta.get_field('description').verbose_name
        price_field_label = job._meta.get_field('price').verbose_name
        self.assertEqual(description_field_label, 'description')
        self.assertEqual(price_field_label, 'price')
        self.assertEqual(job.price, 100.00)
        self.assertEqual(job.contract, self.contract1)
