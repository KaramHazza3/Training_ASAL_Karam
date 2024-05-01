from django.urls import path
from .views import (SignupView, ContractDetailView, ContractsListView,
                    ProfileDetailView, JobsListView, UnPaidJobListView,
                    PayForJobView, BalanceDepositView, BestProfessionView, BestClientsPaidView)
from rest_framework.authtoken import views

urlpatterns = [
    path('signup', SignupView.as_view(), name='signup'),
    path('login', views.obtain_auth_token, name='login'),
    path('contracts/<int:id>', ContractDetailView.as_view(), name='contract-detail'),
    path('contracts/<str:status>', ContractsListView.as_view(), name='contracts-list-status'),
    path('contracts', ContractsListView.as_view(), name='contracts-list-no-param'),
    path('Profile', ProfileDetailView.as_view(), name='current-user-detail'),
    path('jobs', JobsListView.as_view(), name='jobs-current-user'),
    path('jobs/unpaid', UnPaidJobListView.as_view(), name='unpaid-active-jobs-current-user'),
    path('jobs/<int:job_id>/pay', PayForJobView.as_view(), name='pay-for-job'),
    path('balances/deposit/<int:userId>', BalanceDepositView.as_view(), name='balance-deposit'),
    path('jobs/best-profession', BestProfessionView.as_view(), name='best-profession'),
    path('jobs/best-clients', BestClientsPaidView.as_view(), name='best-clients'),
]
