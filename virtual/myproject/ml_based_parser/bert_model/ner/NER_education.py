import pandas as pd

from .NER_Degree import extract_degree
from .NER_university import university_list
from .NER_degree_dates import degree_dates
import logging

logger = logging.getLogger(__name__)


def education_details(dataframe):
    logger.debug("Running NER for education details.")
    degrees = extract_degree(dataframe)
    universities = university_list(dataframe)
    dates = degree_dates(dataframe)
    df1 = pd.DataFrame({'degree': degrees})

    df2 = pd.DataFrame({'universities': universities})

    df3 = pd.DataFrame({'dates': dates})

    final = pd.concat([df1, df2, df3], ignore_index=True, axis=1)

    result = []
    n = len(final.index)

    for i in range(0, n):
        # print (i)
        result.append(list(final.iloc[i].values))
    education = {}
    education["education details"] = result
    logging.debug('NER Education result: {}'.format(education))
    return education
