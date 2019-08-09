import json
import logging

from .pdf_to_text import pdf_to_text
from .doc_to_text import docx_to_text
from .txt_to_json import txt_to_jsn
from .labelpred import predict_label
from .typepred import predict_type
import pandas as pd
from .ner import NER_personal, NER_jobtype, NER_skills, NER_education

logger = logging.getLogger(__name__)


# input the file

def file_to_text(f_name: str) -> list:
    """
    Convert resume file into list of text
    :param f_name: name of file
    :return: list of strings containing lines of resume
    """
    logger.info('Extracting resume texts from file...')
    parse_text = None
    # Parse file
    if f_name.endswith('.pdf'):
        logger.info('File format: .pdf')
        parse_text = pdf_to_text(f_name)
    elif f_name.endswith('.docx') or f_name.endswith('.doc'):
        logger.info('File format: .docx')
        parse_text = docx_to_text(f_name)
    return parse_text


def parse_file(f_name: str):
    """
    Parse Resume file from file
    :param f_name: File Name to be parsed
    :return: Output of parsed info
    """

    parsed_text = file_to_text(f_name)
    json_input = txt_to_jsn(parsed_text)

    # Predict values
    text_label = predict_label(json_input)
    text_type = predict_type(json_input)

    text_type['prediction'] = text_type['prediction'].str[0].apply(lambda x: x.decode('utf-8'))
    text_label['prediction'] = text_label['prediction'].str[0].apply(lambda x: x.decode('utf-8'))

    text_label = text_label.rename(columns={"features": "text", "prediction": "linelabel"})
    text_type = text_type.rename(columns={"features": "newfeatures", "prediction": "linetype"})
    result = pd.concat([text_label, text_type], axis=1)

    logger.info('Running NER on resume...')
    final_result = dict()
    final_result["personal"] = NER_personal.personal_info(result)
    final_result["education"] = NER_education.education_details(result)
    final_result["skills"] = NER_skills.get_skills(result)
    final_result["jobs"] = NER_jobtype.get_jobs(result)

    # final_file = 'fianl_json_output.json'

    # with open(final_file, 'w') as file:
    #     file.write(json.dumps(final_result))

    # result.drop("newfeatures", axis=1, inplace=True)
    # outputjson = result.to_dict(orient='records')
    return final_result
