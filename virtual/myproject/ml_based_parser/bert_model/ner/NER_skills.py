from spacy.matcher import PhraseMatcher
from . import get_spacy_nlp
import logging

spacy_nlp = get_spacy_nlp()
logger = logging.getLogger(__name__)


# nlp = spacy.load('en_core_web_md')
def read_keywords(file):
    line = file.readline().strip()
    listOfKeywords = []
    while line:
        listOfKeywords.append(line)
        line = file.readline().strip()

    return listOfKeywords


def get_skills(dataframe):
    logger.debug("Running NER for skills.")
    df = dataframe
    # df['prediction'] = df['prediction'].str.replace("\[b'", "").str.replace("'\]", "")
    dfm = df['text'][df['linelabel'] == 'skills']

    textff = ""
    for i in dfm:
        textff = textff + i

    textff = textff.replace("\n", "")

    textff = textff.replace("\uf0b7", "")
    textff = textff.lower()
    with open("skills.txt", encoding="utf-8") as f:
        listOfKeywords = read_keywords(f)
    # nlp = spacy.load('en_core_web_sm')
    matcher = PhraseMatcher(spacy_nlp.vocab)
    patterns = [spacy_nlp.make_doc(text) for text in listOfKeywords]
    matcher.add("Skills", None, *patterns)
    doc = spacy_nlp(textff)
    skills = set()
    skill = []

    matches = matcher(doc)
    for match_id, start, end in matches:
        span = doc[start:end]
        if span.text:
            skills.add(span.text)
    skill.append(skills)
    skillset = {}
    skillset["skills"] = skill
    logging.debug('NER Skills result: {}'.format(skills))
    return list(skills)
