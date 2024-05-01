from rest_framework import status
from .test_models import BaseTestCase
from django.urls import reverse


class ProfileViewTest(BaseTestCase):
    def setUp(self):
        self.set_auth_token(self.test_client1)

    def test_profile_details(self):
        url = reverse('current-user-detail')
        response = self.requester.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class ContractsViewTest(BaseTestCase):
    def setUp(self):
        self.set_auth_token(self.test_client1)

    def test_contracts_list(self):
        url = reverse('contracts-list-no-param')
        response = self.requester.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_contracts_list_real_status(self):
        status_arg = 'in_progress'
        url = reverse('contracts-list-status', args=[status_arg])
        response = self.requester.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.json()[0]['status'], 'in_progress')

    def test_contracts_list_unreal_status(self):
        status_arg = 'not_available'
        url = reverse('contracts-list-status', args=[status_arg])
        response = self.requester.get(url)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_contract_real_id(self):
        id = 1
        url = reverse('contract-detail', args=[id])
        response = self.requester.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_contract_unreal_id(self):
        id = 10002
        url = reverse('contract-detail', args=[id])
        response = self.requester.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_contract_unauthorized(self):
        id = 2
        url = reverse('contract-detail', args=[id])
        response = self.requester.get(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class JobViewTest(BaseTestCase):
    def setUp(self):
        self.set_auth_token(self.test_client1)

    def test_jobs_list(self):
        url = reverse('jobs-current-user')
        response = self.requester.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.json()), 4)

    def test_jobs_list_unpaid(self):
        url = reverse('unpaid-active-jobs-current-user')
        response = self.requester.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.json()), 2)

    def test_job_pay(self):
        id = 1
        url = reverse('pay-for-job', args=[id])
        remaining_balance = self.test_client1.balance - self.job1.price
        response = self.requester.post(url)

        # refreshing
        self.test_client1.refresh_from_db()
        self.test_contractor1.refresh_from_db()
        self.job1.refresh_from_db()

        # assertions
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json()['message'], 'Payment successful')
        self.assertEqual(self.test_client1.balance, remaining_balance)
        self.assertGreater(self.test_contractor1.balance, 0)
        self.assertEqual(self.job1.contract.status, 'terminated')
        self.assertEqual(self.job1.paid, 1)

    def test_job_pay_for_paid_job(self):
        id = 6
        url = reverse('pay-for-job', args=[id])
        response = self.requester.post(url)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_job_cant_pay(self):
        self.set_auth_token(self.test_client3)
        id = 5
        url = reverse('pay-for-job', args=[id])
        response = self.requester.post(url)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.json()['error'], 'Insufficient balance')

    def test_contractor_job_pay(self):
        self.set_auth_token(self.test_contractor2)
        id = 1
        url = reverse('pay-for-job', args=[id])
        response = self.requester.post(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(response.json()['error'], 'Permission Denied')

    def test_best_profession_with_valid_dates_and_existed_profession(self):
        url = reverse('best-profession')
        url_with_query_params = f"{url}?start={self.four_days_ago}&end={self.current_date}"
        response = self.requester.get(url_with_query_params)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json()['profession'], 'Graphic Designer')

    def test_best_profession_with_invalid_dates(self):
        url = reverse('best-profession')
        url_with_query_params = f"{url}?start=9000-123-272&end=8777-444-1023"
        response = self.requester.get(url_with_query_params)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.json()['error'],
                         "Date error: time data '9000-123-272' does not match format '%Y-%m-%d'")

    def test_best_profession_with_start_date_greater_than_end(self):
        url = reverse('best-profession')
        url_with_query_params = f"{url}?start={self.current_date}&end={self.four_days_ago}"
        response = self.requester.get(url_with_query_params)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.json()['error'], 'Date error: The start date must not be later than the end date.')

    def test_best_profession_with_valid_dates_and_not_existed_profession(self):
        self.set_auth_token(self.test_client3)
        url = reverse('best-profession')
        url_with_query_params = f"{url}?start={self.ten_days_ago}&end={self.seven_days_ago}"
        response = self.requester.get(url_with_query_params)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.json()['error'], 'No profession found.')

    def test_best_clients_with_valid_dates_without_limit(self):
        url = reverse('best-clients')
        url_with_query_params = f"{url}?start={self.four_days_ago}&end={self.current_date}"
        response = self.requester.get(url_with_query_params)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertLessEqual(len(response.json()), 2)

    def test_best_clients_with_valid_dates_with_limit(self):
        url = reverse('best-clients')
        url_with_query_params = f"{url}?start={self.four_days_ago}&end={self.current_date}&limit=5"
        response = self.requester.get(url_with_query_params)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.json()), 3)
