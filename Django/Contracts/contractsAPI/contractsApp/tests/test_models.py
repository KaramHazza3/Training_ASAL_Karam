from django.test import TestCase
from rest_framework.authtoken.models import Token
from rest_framework.test import APIClient

from ..models import Profile, Contract, Job


class BaseTestCase(TestCase):
    fixtures = ['profiles.json', 'contracts.json', 'jobs.json']

    def setUp(self):
        self.set_auth_token(Profile.objects.get(username='testclient'))

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
        self.assertEqual(profile.type, 'Client')
        self.assertEqual(profile.balance, 500.00)

    def test_created_contractor(self):
        profile = Profile.objects.get(username='testcontractor')
        user_type_field_label = profile._meta.get_field('type').verbose_name
        self.assertEqual(user_type_field_label, 'type')
        self.assertEqual(profile.profession, 'Graphic Designer')
        self.assertEqual(profile.type, 'Contractor')
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
        self.assertEqual(job.contract.id, 1)
