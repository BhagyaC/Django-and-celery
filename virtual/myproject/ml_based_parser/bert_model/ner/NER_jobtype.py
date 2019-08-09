from spacy.matcher import PhraseMatcher
from . import get_spacy_nlp
import logging

spacy_nlp = get_spacy_nlp()
logger = logging.getLogger(__name__)


def read_keywords(file):
    line = file.readline().strip()
    listOfKeywords = []
    while line:
        listOfKeywords.append(line)
        line = file.readline().strip()

    return listOfKeywords


def get_jobs(dataframe):
    logger.debug('Running NER for personal jobs.')
    df = dataframe
    # df['prediction'] = df['prediction'].str.replace("\[b'", "").str.replace("'\]", "")
    dfm = df['text'][df['linelabel'] == 'experience']

    textff = ""
    for i in dfm:
        textff = textff + i

    textff = textff.replace("\n", "")

    textff = textff.replace("\uf0b7", "")
    textff = textff.lower()
    with open("jobs.txt", encoding="utf-8") as f:
        list_of_keywords = read_keywords(f)
    # nlp = spacy.load('en_core_web_sm')
    matcher = PhraseMatcher(spacy_nlp.vocab)
    patterns = [spacy_nlp.make_doc(text) for text in list_of_keywords]
    matcher.add("jobs", None, *patterns)
    doc = spacy_nlp(textff)
    jobs = set()
    job = []

    matches = matcher(doc)
    for match_id, start, end in matches:
        span = doc[start:end]
        if span.text:
            jobs.add(span.text)
    job.append(jobs)
    jobset = {}
    jobset["job_roles"] = job
    logging.debug('NER Job result: {}'.format(jobs))
    return list(jobs)
