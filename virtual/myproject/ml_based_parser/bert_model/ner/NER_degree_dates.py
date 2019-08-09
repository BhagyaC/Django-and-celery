from . import get_spacy_nlp

spacy_nlp = get_spacy_nlp()


# nlp = spacy.load("en_core_web_md")

def degree_dates(dataframe):
    df = dataframe
    dfm = df.loc[df['linelabel'] == 'education', 'text']
    item = dfm.items()
    list_items = []
    for i, value in item:
        list_items.append(value)
    # nlp = spacy.load("en_core_web_sm")
    dates_of_edu = []
    for i in list_items:
        size = 0
        i = i.replace("\uf0b7", "")
        i = i.replace("\n", "")
        i = i.lower()
        doc = spacy_nlp(i)
        # print("line:", i)
        for ent in doc.ents:
            # print(ent.text, ent.start_char, ent.end_char, ent.label_)
            if ent.label_ == "DATE":
                dates_of_edu.append(ent.text)
    return dates_of_edu
