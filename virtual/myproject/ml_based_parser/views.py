import json
import logging

from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view
from rest_framework import status
from django.http.response import JsonResponse
from rest_framework.request import Request
from .util import parser_util
from .forms import ResumeUploadForm
from prometheus_client import start_http_server, Summary
import random
import time

# Create a metric to track time spent and requests made.
REQUEST_TIME = Summary('parse_file_request_processing_seconds', 'Time spent processing request')

logger = logging.getLogger(__name__)


@api_view(['GET'])
def health_check(request: Request) -> JsonResponse:
    """
    Health check for api endpoint
    :param request: Django Rest Framework Request object
    :return: Response with HTTP 200 if service is up.
    """

    logger.info('API Health Check called')
    data = {
        'result': 'success',
        'text': 'Health Check Successful!'
    }
    return JsonResponse(data, status=status.HTTP_200_OK)


@REQUEST_TIME.time()
@csrf_exempt
@api_view(['POST'])
def parse_resume_file(request: Request) -> JsonResponse:
    """
    API endpoint to parse resume file.
    'client_id' and 'file' params is needed to parse resume
    :param request: Django Rest Framework Request object
    :return: a JSON output of parsed resume
    """
    logger.info('API Parse Resume Called')
    # confirms file is in request
    if 'document' not in request.FILES:
        req_err_no_file_param = {
            'result': 'error',
            'text': 'file not found in request. Resume file is required to parse resume'
        }
        return JsonResponse(req_err_no_file_param, status=status.HTTP_400_BAD_REQUEST)

    # confirms candidate_id is in request
    if 'candidate_id' not in request.data or not request.data['candidate_id']:
        req_err_no_candidate_id_param = {
            'result': 'error',
            'text': 'candidate_id not found/empty in request. candidate_id is required to parse resume.'
        }
        return JsonResponse(req_err_no_candidate_id_param, status=status.HTTP_400_BAD_REQUEST)

    # Perform django model additional validation e.g. max length based on model
    resume_form = ResumeUploadForm(request.POST, request.FILES)
    if not resume_form.is_valid():
        # Get fields that contain errors
        fields_errors = json.loads(resume_form.errors.as_json())

        for field in fields_errors.keys():
            req_error = {
                'result': 'error',
                'text': '{field}: {message}'.format(field=field, message=fields_errors[field][0]['message'])
            }
            return JsonResponse(req_error, status=status.HTTP_400_BAD_REQUEST)

    # Automatically handles file upload, builds the absolute path from the upload, treats filename conflicts
    resume_doc = resume_form.save()
    try:
        parsed_resume = parser_util.parse_candidate_resume(resume_doc.id)
        response_success = {
            'result': 'success',
            'text': 'parse successful',
            'resume_details': parsed_resume,
        }
        return JsonResponse(response_success, status=status.HTTP_200_OK)
    except Exception as e:
        logger.exception(e)
        response_error = {
            'result': 'error',
            'text': 'Error parsing resume: {}'.format(e)
        }
        return JsonResponse(response_error, status=status.HTTP_200_OK)


@csrf_exempt
@api_view(['POST'])
def get_candidate_parsed_resume(request: Request) -> JsonResponse:
    """
    API endpoint to get parsed resumes of candidates.
    if 'candidate_id' is not provided, returns all parsed resume info.
    :param request: Django Rest Framework Request object
    :return: a list of JSON
    """

    logger.info('API Get Candidate Parsed Resume Called')

    if 'candidate_id' in request.data and request.data['candidate_id']:
        candidate_id = request.data['candidate_id']
    else:
        candidate_id = None

    candidate_info = mock_get_candidate_info(candidate_id)

    result = {
        'result': 'success',
        'text': '!',
        'candidate_info': candidate_info
    }
    return JsonResponse(result, status=status.HTTP_200_OK)


def mock_get_candidate_info(candidate_id):
    data = [
        {
            'candidate_id': 1,
            'resume_info': {
                "education_keys": {
                    "institute": "InstituteName",
                    "location": "InstituteLocation",
                    "degree": "Degree",
                    "major": "Major",
                    "class": "Class",
                    "graduation_month": "GraduationMonth",
                    "graduation_year": "GraduationDate",
                    "gpa": "4.0"
                },
                "experience_keys": {
                    "type": "type",
                    "position": "JobTitle",  # Job Title ?
                    "location": "JobLocation",
                    "employer": "Employer",
                    "start_date": "StartDate",
                    "end_date": "EndDate"
                },
                "phone": "Phone",
                "nationality": "Nationality",
                "postal_code": "ZipCode",
                "preferred_location": "PreferredLocation",
                "language": "LanguageKnown",
                "date_of_birth": "DateOfBirth"
            },
            'date_created': 'DD-MM-YYYY'
        }
    ]
    return data
