import json
import logging

from django.http.response import JsonResponse
from rest_framework.request import Request
from rest_framework.decorators import api_view
from celery import shared_task
from .utils import parser_util


logger = logging.getLogger(__name__)


@shared_task
def parser():

    logger.info('API Parse Resume Called')
    # confirms file is in request
    parsed_data = dummy_resume_parser()

    result = {
        'ResumeParserData': parsed_data
    }
    return result


def dummy_resume_parser():
    data = {
        "parsingDate": "12/07/2019 10:15:12",
        "personal": {
            "Nationality": "",
            "Industry": "Education",
            "Phone": "",
            "Address": "2002 Front Range Way, Fort Collins, CO, 80525",
            "SubIndustry": "Teaching/Professor/Lecturer",
            "PreferredLocation": "",
            "LanguageKnown": "",
            "LastName": "Smith",
            "Gender": "",
            "Description": "Functional Resume Sample\n\n\t  John W. Smith\n2002 Front Range Way Fort Collins, CO 80525\njwsmith@colostate.edu\n\nCareer Summary\nFour years experience in early childhood development with a diverse background in the care of special needs children and adults.\nAdult Care Experience\n\t  .\t  Determined work placement for 150 special needs adult clients.\n\t  .\t  Maintained client databases and records.\n\t  .\t  Coordinated client contact with local health care professionals on a monthly basis.\n\t  .\t  Managed 25 volunteer workers.\n\nChildcare Experience\n\t  .\t  Coordinated service assignments for 20 part-time counselors and 100 client families.\n\t  .\t  Oversaw daily activity and outing planning for 100 clients.\n\t  .\t  Assisted families of special needs clients with researching financial assistance and healthcare.\n\t  .\t  Assisted teachers with managing daily classroom activities.\n\t  .\t  Oversaw daily and special student activities.\n\nEmployment History\n\n1999-2002\t  Counseling Supervisor, The Wesley Center, Little Rock, Arkansas.\n1997-1999\t  Client Specialist, Rainbow Special Care Center, Little Rock, Arkansas\n1996-1997\t  Teacher's Assistant, Cowell Elementary, Conway, Arkansas\n\nEducation\nUniversity of Arkansas at Little Rock, Little Rock, AR\n\n.\t  BS in Early Childhood Development ( 1999 ) \n.\t  BA in Elementary Education ( 1998 ) \n.\t  GPA ( 4.0 Scale ) : Early Childhood Development - 3.8 , Elementary Education - 3.5 ,\n Overall 3.4.\n.\t  Dean's List, Chancellor's List",
            "FirstName": "John",
            "Email": "bhagya+9127@impress.ai",
            "ZipCode": "80525",
            "CountryOfResidence": ""
        },
        "education": [
            {
                "GraduationDate": "1999",
                "Class": "",
                "GraduationMonth": "Dec",
                "InstituteLocation": "Little Rock,AR",
                "InstituteName": "University of Arkansas at Little Rock",
                "GPA": "",
                "id": 1,
                "Major": "Early Childhood Development",
                "Degree": "BS"
            },
            {
                "GraduationDate": "1998",
                "Class": "",
                "GraduationMonth": "Dec",
                "InstituteLocation": "",
                "InstituteName": "",
                "GPA": "4.0",
                "id": 2,
                "Major": "Elementary Education",
                "Degree": "BA"
            }
        ],
        "formatVersion": 1.0,
        "website": [
            {
                "type": "",
                "url": "",
                "id": 1
            }
        ],
        "recommendations": [
            {
                "PersonName": "",
                "Description": "",
                "PositionTitle": "",
                "CompanyName": "",
                "id": 1,
                "Relation": ""
            }
        ],
        "publications": [],
        "experience": [
            {
                "StartDate": "01/01/1999",
                "EndDate": "31/12/2002",
                "Description": "",
                "JobLocation": "Little Rock,Arkansas,USA",
                "JobTitle": "Counseling Supervisor",
                "id": 1,
                "Employer": "The Wesley Center"
            },
            {
                "StartDate": "01/01/1997",
                "EndDate": "31/12/1999",
                "Description": "",
                "JobLocation": "Little Rock,Arkansas,USA",
                "JobTitle": "Client Specialist",
                "id": 2,
                "Employer": "Rainbow Special Care Center"
            },
            {
                "StartDate": "01/01/1996",
                "EndDate": "31/12/1997",
                "Description": "",
                "JobLocation": "Conway,Arkansas,USA",
                "JobTitle": "Teachers Assistant",
                "id": 3,
                "Employer": "Cowell Elementary"
            }
        ],
        "achievements": [],
        "skills": [
            "Determined",
            "Managing",
            "Planning",
            "Researching Financial Assistance",
            "Early Childhood Development",
            "Student Activities",
            "Client Databases",
            "Care Experience",
            "Client Contact",
            "Childcare"
        ],
        "resumeFullText": "Functional Resume Sample\n\n\t  John W. Smith\n2002 Front Range Way Fort Collins, CO 80525\njwsmith@colostate.edu\n\nCareer Summary\nFour years experience in early childhood development with a diverse background in the care of special needs children and adults.\nAdult Care Experience\n\t  .\t  Determined work placement for 150 special needs adult clients.\n\t  .\t  Maintained client databases and records.\n\t  .\t  Coordinated client contact with local health care professionals on a monthly basis.\n\t  .\t  Managed 25 volunteer workers.\n\nChildcare Experience\n\t  .\t  Coordinated service assignments for 20 part-time counselors and 100 client families.\n\t  .\t  Oversaw daily activity and outing planning for 100 clients.\n\t  .\t  Assisted families of special needs clients with researching financial assistance and healthcare.\n\t  .\t  Assisted teachers with managing daily classroom activities.\n\t  .\t  Oversaw daily and special student activities.\n\nEmployment History\n\n1999-2002\t  Counseling Supervisor, The Wesley Center, Little Rock, Arkansas.\n1997-1999\t  Client Specialist, Rainbow Special Care Center, Little Rock, Arkansas\n1996-1997\t  Teacher's Assistant, Cowell Elementary, Conway, Arkansas\n\nEducation\nUniversity of Arkansas at Little Rock, Little Rock, AR\n\n.\t  BS in Early Childhood Development ( 1999 ) \n.\t  BA in Elementary Education ( 1998 ) \n.\t  GPA ( 4.0 Scale ) : Early Childhood Development - 3.8 , Elementary Education - 3.5 ,\n Overall 3.4.\n.\t  Dean's List, Chancellor's List"
    }
    return data
@shared_task
def parse_resume(resume_parse_id: str):
    try:
        parsed_resume = parser_util.parse_candidate_resume(resume_parse_id)
        response_success = {
            'result': 'success',
            'text': 'parse successful',
            'resume_details': parsed_resume,
        }
        return (response_success)
    except Exception as e:
        logger.exception(e)
        response_error = {
            'result': 'error',
            'text': 'Error parsing resume: {}'.format(e)
        }
        return (response_error)
