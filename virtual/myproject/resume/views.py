from django.shortcuts import render

import json
import logging

from django.http.response import JsonResponse
from rest_framework.request import Request
from rest_framework.decorators import api_view
from .tasks import parse_resume


from django.views.decorators.csrf import csrf_exempt

from rest_framework import status
from .forms import ResumeUploadForm
from prometheus_client import start_http_server, Summary
import random
import time

# Create your views here.

logger = logging.getLogger(__name__)


@api_view(['POST'])
def async_parser(request):

    logger.info('API Parse Resume Called')
    
    if 'document' not in request.FILES:
        request_error = {
            'result': 'error',
            'text': 'file not found in request. Resume file is required to parse resume'
        }
        return JsonResponse(request_error)
    parse_resume_file.delay()
    return JsonResponse({"result": "success"})


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
        parse_resume(resume_doc.id)
        response_success = {
            'result': 'success',
            'text': 'parse successful',
        }
        return JsonResponse(response_success, status=status.HTTP_200_OK)
    except Exception as e:
        logger.exception(e)
        response_error = {
            'result': 'error',
            'text': 'Error parsing resume: {}'.format(e)
        }
        return JsonResponse(response_error, status=status.HTTP_200_OK)


