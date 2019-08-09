from spacy.matcher import PhraseMatcher
from . import get_spacy_nlp

spacy_nlp = get_spacy_nlp()


# nlp = spacy.load("en_core_web_md")
def read_keywords(file):
    line = file.readline().strip()
    listOfKeywords = []
    while line:
        listOfKeywords.append(line)
        line = file.readline().strip()

    return listOfKeywords


def university_list(dataframe):
    df = dataframe
    # df['prediction'] = df['prediction'].str.replace("\[b'", "").str.replace("'\]", "")
    # cross check that the colomn name matches with result from pediction
    dfm = df.loc[df['linelabel'] == 'education', 'text']
    item = dfm.items()
    list_items = []
    for i, value in item:
        list_items.append(value)
    with open("university.txt", encoding="utf-8") as f:
        listOfKeywords = read_keywords(f)
    # nlp = spacy.load('en_core_web_sm')
    matcher = PhraseMatcher(spacy_nlp.vocab)
    patterns = [spacy_nlp.make_doc(text) for text in listOfKeywords]
    matcher.add("University", None, *patterns)
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
        if matches:
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
