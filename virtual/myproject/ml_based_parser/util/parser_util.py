import logging

from ml_based_parser.models import ResumeParse
from django.db.models.functions import Now
from ml_based_parser.bert_model import bert_parser

logger = logging.getLogger(__name__)


def parse_candidate_resume(resume_parse_id: str):
    """
    Parse resume document and returns entities found from resume
    :param resume_parse_id: id of current resume parse
    :return: JSON of entities found
    """

    # Celery task for resume parsing
    resume = ResumeParse.objects.get(pk=resume_parse_id)
    document = ResumeParse.objects.get(pk=resume_parse_id).document

    # Get parser and parse resume. Time duration of parsing document
    resume.time_start = Now()
    logger.info('Parsing resume for candidate_id: {}'.format(resume.candidate_id))
    results = bert_parser.parse_file(document.url)
    logger.info('Parsing resume completed for candidate_id: {}'.format(resume.candidate_id))
    resume.time_end = Now()

    # Delete resume from tmp/ folder
    ResumeParse.objects.get(pk=resume_parse_id).document.delete(save=True)
    resume.save()
    # Return output

    return results
