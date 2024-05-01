from django.shortcuts import get_object_or_404
from drf_spectacular.types import OpenApiTypes
from rest_framework import generics, permissions, status
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import ProfileSerializer, ContractSerializer, JobSerializer, BalanceDepositSerializer
from .services import *
from drf_spectacular.utils import extend_schema, OpenApiParameter, OpenApiResponse


class SignupView(generics.CreateAPIView):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer


class ContractDetailView(generics.RetrieveAPIView):
    serializer_class = ContractSerializer
    permission_classes = [permissions.IsAuthenticated]
    queryset = Contract.objects.all()
    lookup_field = 'id'

    def retrieve(self, request, *args, **kwargs):
        user_id = self.request.user.id
        contract = self.get_object()
        if contract.client.id != user_id and contract.contractor.id != user_id:
            return Response('Access Denied', status=status.HTTP_403_FORBIDDEN)
        return super().retrieve(self, request, *args, **kwargs)


class ContractsListView(generics.ListAPIView):
    serializer_class = ContractSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        requested_status = self.kwargs.get('status', None)
        try:
            return filter_contracts_by_status_and_user(self.request.user.id, requested_status)
        except ValueError as e:
            raise ValidationError(str(e))

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        if not queryset.exists():
            return Response({'error': 'No contracts found.'}, status=status.HTTP_404_NOT_FOUND)
        return super().list(request, *args, **kwargs)


class ProfileDetailView(generics.RetrieveAPIView):
    serializer_class = ProfileSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        user_id = self.request.user.id
        return get_object_or_404(Profile, id=user_id)


class JobsListView(generics.ListAPIView):
    serializer_class = JobSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return get_jobs_for_user(self.request.user.id)


class UnPaidJobListView(generics.ListAPIView):
    serializer_class = JobSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return get_jobs_for_user(self.request.user.id, paid=False, status='in_progress')

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        if not queryset.exists():
            return Response({'error': 'No unpaid jobs found.'}, status=status.HTTP_404_NOT_FOUND)
        return super().list(request, *args, **kwargs)


class PayForJobView(generics.CreateAPIView):
    permission_classes = [permissions.IsAuthenticated]

    @extend_schema(
        responses={
            200: OpenApiResponse(description="Payment successful", response=OpenApiTypes.STR),
            400: OpenApiResponse(description="Invalid request", response=OpenApiTypes.STR),
            403: OpenApiResponse(description="Permission denied", response=OpenApiTypes.STR)
        },
        description="Process a payment for a job. Returns a success message or an error.",
        summary="Pay for a contract job"
    )
    def post(self, request, *args, **kwargs):
        if request.user.user_type == 'Contractor':
            return Response({'error': 'Permission Denied'}, status=status.HTTP_403_FORBIDDEN)

        job_id = kwargs.get('job_id')
        try:
            message = process_job_payment(request.user.id, job_id)
            return Response({'message': message}, status=status.HTTP_200_OK)
        except Job.DoesNotExist:
            return Response({'error': 'Job not found'}, status=status.HTTP_404_NOT_FOUND)
        except ValueError as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)


class BalanceDepositView(generics.CreateAPIView):
    serializer_class = BalanceDepositSerializer
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, *args, **kwargs):
        amount = Decimal(request.data.get('amount', 0))

        try:
            message = deposit_to_balance(request.user.id, amount)
            return Response({'message': message}, status=status.HTTP_200_OK)
        except Profile.DoesNotExist:
            return Response({'error': 'Client not found'}, status=status.HTTP_404_NOT_FOUND)
        except ValueError as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)


def validate_dates(start_date_str, end_date_str):
    try:
        start_date = datetime.strptime(start_date_str, '%Y-%m-%d').date()
        end_date = datetime.strptime(end_date_str, '%Y-%m-%d').date()
        if start_date > end_date:
            raise ValueError("The start date must not be later than the end date.")
        return start_date, end_date
    except ValueError as e:
        raise ValueError(f"Date error: {str(e)}")


class BestProfessionView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    @extend_schema(
        parameters=[
            OpenApiParameter(name='start', description='Start date in YYYY-MM-DD format', required=True, type=str),
            OpenApiParameter(name='end', description='End date in YYYY-MM-DD format', required=True, type=str)
        ]
    )
    def get(self, request):
        start_date_str = request.query_params.get('start')
        end_date_str = request.query_params.get('end')

        if not start_date_str or not end_date_str:
            return Response({'error': "Both 'start' and 'end' date parameters are required."},
                            status=status.HTTP_400_BAD_REQUEST)

        try:
            start_date, end_date = validate_dates(start_date_str, end_date_str)
        except ValueError as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

        profession = get_best_profession(start_date, end_date)
        if profession:
            return Response({'profession': profession['profession']})
        return Response({'error': 'No profession found.'}, status=status.HTTP_404_NOT_FOUND)


class BestClientsPaidView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    @extend_schema(
        parameters=[
            OpenApiParameter(name='start', description='Start date in YYYY-MM-DD format', required=True, type=str),
            OpenApiParameter(name='end', description='End date in YYYY-MM-DD format', required=True, type=str),
            OpenApiParameter(name='limit', type=int, description="The number of results to return", required=False)
        ]
    )
    def get(self, request):
        start_date_str = request.query_params.get('start')
        end_date_str = request.query_params.get('end')

        if not start_date_str or not end_date_str:
            return Response({'error': "Both 'start' and 'end' date parameters are required."},
                            status=status.HTTP_400_BAD_REQUEST)

        try:
            start_date, end_date = validate_dates(start_date_str, end_date_str)
        except ValueError as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

        clients = get_best_clients(start_date, end_date, int(request.query_params.get('limit', 2)))
        serialized_data = [
            {
                'id': client['contract__client__id'],
                'fullName': client['fullName'],
                'paid': client['total_paid']
            }
            for client in clients
        ]

        if serialized_data:
            return Response(serialized_data)
        else:
            return Response({'error': 'No clients found.'}, status=status.HTTP_404_NOT_FOUND)
