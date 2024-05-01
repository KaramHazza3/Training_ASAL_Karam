# from django.urls import reverse
# from rest_framework import status
# from rest_framework.test import APITestCase
# from rest_framework.authtoken.models import Token
# from .models import Job, Contract, Profile
#
#
# class BaseTestCase(APITestCase):
#     @classmethod
#     def setUpTestData(cls):
#         cls.client = Profile.objects.create_user(username='testclient', email='testclient@mail.com',
#                                                  password='password',
#                                                  first_name='John', last_name='Doe', profession='Software Developer',
#                                                  user_type='Client', balance=500.00)
#
#         cls.contractor = Profile.objects.create_user(username='contractor1', email='contractor1@example.com',
#                                                      password='password', first_name='Jane', last_name='Smith',
#                                                      profession='Graphic Designer', user_type='Contractor',
#                                                      balance=0.00)
#
#         # cls.contract = Contract.objects.create(terms='Terms for test contract ', status='in_progress',
#         #                                        client=self.client,
#         #                                        contractor=cls.contractor)
#         #
#         # cls.job1 = Job.objects.create(description='Description for test job 1', price=100.00, contract=cls.contract)
#         # cls.job2 = Job.objects.create(description='Description for test job 2', price=150.00, contract=cls.contract)
#
#
# class ProfileTests(BaseTestCase):
#     def client_login(self):
#         self.token = Token.objects.create(user=self.client)
#         self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
#
#     def test_profile_details(self):
#         url = reverse('Profile')
#         response = self.client.get(url)
#         self.assertEqual(response.status_code, status.HTTP_200_OK)
