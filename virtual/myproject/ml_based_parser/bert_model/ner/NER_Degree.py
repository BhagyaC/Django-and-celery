from spacy.matcher import PhraseMatcher
from . import get_spacy_nlp
import logging

spacy_nlp = get_spacy_nlp()
logger = logging.getLevelName(__name__)


# nlp = spacy.load("en_core_web_md")

def read_keywords(file):
    line = file.readline().strip()
    list_of_keywords = []
    while line:
        list_of_keywords.append(line)
        line = file.readline().strip()

    return list_of_keywords


def extract_degree(dataframe):
    df = dataframe
    # df['prediction'] = df['prediction'].str.replace("\[b'", "").str.replace("'\]", "")
    # cross check that the colomn name matches with result from pediction
    dfm = df.loc[df['linelabel'] == 'education', 'text']
    item = dfm.items()
    list_items = []
    for i, value in item:
        list_items.append(value)
    with open("degree.txt", encoding="utf-8") as f:
        list_of_keywords = read_keywords(f)
    # nlp = spacy.load('en_core_web_sm')
    matcher = PhraseMatcher(spacy_nlp.vocab)
    patterns = [spacy_nlp.make_doc(text) for text in list_of_keywords]
    # logger.debug(patterns)
    matcher.add("Degree", None, *patterns)
    final_list = []
    for i in list_items:
        size = 0
        i = i.replace("\uf0b7", "")
        i = i.replace("\n", "")
        i = i.lower()
        doc = spacy_nlp(i)
        # print("line:", i)
        matches = matcher(doc)
        # print(matches)
        for match_id, start, end in matches:
            span = doc[start:end]
            # final_list.append(span.text)
            # print("predicted :", span.text)
            if len(span.text) > size:
                final = span.text
                # print("the text", final)
                size = len(span.text)
                # print("the size ", size)
                # print("final one", final)
                final_list.append(final)
        # print("*********added")
    return final_list
