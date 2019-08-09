import json


# give the name of json file to be created
def txt_to_jsn(resume_lines: list):
    """
    Converts lines in resume into json format
    :param resume_lines: List of strings containing lines of resume
    :return: JSON format of lines
    """
    # For developing
    # json_file = 'bertinput.json'
    converted_json = []
    # with open(json_file, 'w') as fp:
    for line in resume_lines:
        data = dict()
        sentence = line
        if (sentence.strip(
                "\n").strip() and sentence != "\u00a0\n" and sentence != "\f\u00a0\n" and sentence != "\f" and sentence != "\f"):
            data['text'] = sentence
            data['linelabel'] = 0
            data['linetype'] = 0
            line_new = json.dumps(data) + '\n'
            converted_json.append(line_new)
            # fp.write(line_new)
    return converted_json
