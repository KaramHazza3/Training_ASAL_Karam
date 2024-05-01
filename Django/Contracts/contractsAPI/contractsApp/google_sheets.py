from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build
from django.conf import settings


def get_service():
    scopes = ['https://www.googleapis.com/auth/spreadsheets']
    credentials = Credentials.from_service_account_file(
        settings.GOOGLE_SHEET_API_CREDENTIALS, scopes=scopes
    )
    service = build('sheets', 'v4', credentials=credentials)
    return service


def append_row(values):
    service = get_service()
    body = {
        'values': [values]
    }
    result = service.spreadsheets().values().append(
        spreadsheetId=settings.GOOGLE_SHEET_ID,
        range='A1:D100',
        valueInputOption='USER_ENTERED',
        insertDataOption='INSERT_ROWS',
        body=body
    ).execute()
    return result
